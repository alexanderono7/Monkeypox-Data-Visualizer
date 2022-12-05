from collections import defaultdict
import pycountry_convert as pc
import pycountry
import subprocess
import psycopg2
import hashlib
import csv

# Alexander Ono - 12/4/2022
header = ['location', 'iso_code', 'date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'new_cases_smoothed', 'new_deaths_smoothed', 'new_cases_per_million', 'total_cases_per_million', 'new_cases_smoothed_per_million', 'new_deaths_per_million', 'total_deaths_per_million', 'new_deaths_smoothed_per_million']
database = 'finalproject'

# Creating dictionary of alpha3 -> alpha2 country codes
alpha_codes = dict()
for country in list(pycountry.countries):
    alpha_codes[country.alpha_3] = country.alpha_2

# Given the alpha 3 ISO code of a country, return its corresponding alpha 2 ISO code
def getAlpha2(alpha3:str) -> str:
    return alpha_codes[alpha3]

# Given the alpha 3 ISO code of a country, return its continent
def getContinent(country_alpha3:str) -> str:
    country_alpha2 = getAlpha2(country_alpha3)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

# Given a string argument, hash it into a unique value (for usage as a primary key)
def getHash(arg:str) -> str:
    hash_object = hashlib.md5(str.encode(arg))
    return hash_object.hexdigest()

# Parse monkeypox data csv file
def print_csv():
    with open('owid-monkeypox-data.csv', newline='') as csvfile:
        monkey_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i,row in enumerate(monkey_reader):
            if i is not 0:
                print(' | '.join(row))
    print(header)

# Populate db with csv data from W.H.O.
def populate_db():
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()
    with open('owid-monkeypox-data.csv', newline='') as csvfile:
        monkey_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i,row in enumerate(monkey_reader):
            if i is not 0:
                date = str("\'" + row[2] + "\'")
                nationname = row[0]

                alpha3 = row[1]
                if(alpha3 == 'OWID_WRL'):
                    continue

                continent = getContinent(alpha3) # we must convert from alpha2 -> alpha3 because the Javascript D3 library operates using alpha3 codes, but the pyCountry module uses alpha2.

                conf_cases = row[3]
                conf_deaths = row[4]
                new_cases = row[5]
                new_deaths = row[6]

                nationkey = getHash(nationname + date)
                continentkey = getHash(getContinent(alpha3) + date)
                glokey = getHash('GLO' + date)

                # If the row already exists: add new values to its existing values. Create the row with attrs initialized to new values if it doesn't exist.
                # Intendend to be used for GLOBAL and CONTINENT.
                conditional_insert_query = '''
                do $$
                BEGIN
                IF EXISTS (SELECT * FROM {relation} WHERE {keyattr} = \'{key}\' ) THEN
                    UPDATE {relation} 
                    SET {prefix}_CONFIRMEDCASES = {prefix}_CONFIRMEDCASES + {cc_val},
                        {prefix}_CONFIRMEDDEATHS = {prefix}_CONFIRMEDDEATHS + {cd_val},
                        {prefix}_NEWCASES = {prefix}_NEWCASES + {nc_val},
                        {prefix}_NEWDEATHS = {prefix}_NEWDEATHS + {nd_val}
                    WHERE {keyattr} = \'{key}\';
                ELSE
                    INSERT INTO {relation} ({cname}{keyattr}, {prefix}_CONFIRMEDCASES, {prefix}_CONFIRMEDDEATHS, {prefix}_NEWCASES, {prefix}_NEWDEATHS{foreignkey})
                    VALUES ({cnameval}\'{key}\', {cc_val}, {cd_val}, {nc_val}, {nd_val}{foreign});
                END IF;
                end $$
                '''

                global_insert = conditional_insert_query.format(prefix='G', relation='GLOBAL', keyattr='G_GLOBALKEY', key=glokey, cc_val=conf_cases, cd_val=conf_deaths, nc_val=new_cases, nd_val=new_deaths, foreignkey="", foreign="", cname="",cnameval="")
                continent_insert = conditional_insert_query.format(prefix='C', relation='CONTINENT', keyattr='C_CONTINENTKEY', key=continentkey, cc_val=conf_cases, cd_val=conf_deaths, nc_val=new_cases, nd_val=new_deaths, foreignkey=", C_GLOBALKEY", foreign=", \'"+glokey+"\'",cname="C_NAME, ",cnameval="\'"+continent+"\', ")

                # If date entry doesn't exist yet, create it. Otherwise do nothing.
                date_insert = f'''
                do $$
                BEGIN
                IF NOT EXISTS (SELECT * FROM D_DATE WHERE D_DATEKEY = {date}) THEN
                    INSERT INTO D_DATE (D_DATEKEY, D_GLOBALKEY)
                    VALUES ({date}, '{glokey}');
                END IF;
                end $$
                '''

                # Regular insertion query for nation.
                nation_insert = f'''
                INSERT INTO nation (N_NATIONKEY, N_NAME, N_CODE, N_CONFIRMEDCASES, N_CONFIRMEDDEATHS, N_NEWCASES, N_NEWDEATHS, N_CONTKEY, N_DATEKEY)
                VALUES (\'{nationkey}\', \'{nationname}\', \'{alpha3}\', {conf_cases}, {conf_deaths}, {new_cases}, {new_deaths}, \'{continentkey}\', {date});
                '''
                cur.execute(global_insert)
                cur.execute(continent_insert)
                cur.execute(date_insert)
                cur.execute(nation_insert)
    conn.commit()
    cur.close()
    conn.close()

# Read out all tuples from 'nation' relation
def access_db():
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()
    cur.execute('select * from nation')
    for x in cur:
        print(x)
    #print(dir(cur))
    #print(type(cur))
    cur.close()
    conn.close()

# remove all rows from 'nation' relation
def clear_nation():
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()
    delete_query = f'''
    DELETE FROM nation;
    '''
    cur.execute(delete_query)
    conn.commit()
    cur.close()
    conn.close()

# Update a the data for a specific country at a specific instance in time
def update_db(nkey, date, attr, value):
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()

    update_query = f'''
    UPDATE nation
    set {attr} = {value}
    where n_name = \'{nkey}\' and date = \'{date}\'
    '''

    cur.execute(update_query)
    conn.commit()
    cur.close()
    conn.close()

# Query data of a country at a given date 
def select_country_time(nkey, date):
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()
    update_query = f'''
    select *
    from nation
    where n_name=\'{nkey}\' and date = \'{date}\';
    '''
    cur.execute(update_query)
    for x in cur:
        print(x)
    cur.close()
    conn.close()

# Select all values of certain country
def select_country_all(nkey):
    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()
    update_query = f'''
    select *
    from nation
    where n_name = \'{nkey}\';
    '''
    cur.execute(update_query)
    for x in cur:
        print(x)
    cur.close()
    conn.close()

# probably going to be used the most frequently
def query_nations(attr, date):
    # attr should be either 'cc', 'cd', 'nc', or 'nd'
    # date should be in YYYY-MM-DD format
    column = "?"
    if(attr=='cc'):
        column = 'CONFIRMEDCASES'
    elif(attr=='cd'):
        column = 'CONFIRMEDDEATHS'
    elif(attr=='nc'):
        column = 'NEWCASES'
    elif(attr=='nd'):
        column = 'NEWDEATHS'

    conn = psycopg2.connect(dbname=database)
    cur = conn.cursor()

    nation_query = f'''
    select n_code, N_{column}
    from nation
    where n_datekey = \'{date}\'
    '''
    cur.execute(nation_query)
    idk = 'code,total\n'
    for x in cur:
        idk += x[0] + ',' + str(x[1]) + "\n"
    writeCsv(idk)
    print(idk)
    cur.close()
    conn.close()

def writeCsv(query_result):
    with open('buffer.csv','w') as file:
        file.write(query_result)
subprocess.run('clear')
#query_nations('cc', '2022-11-20')
# Presentation/Demo begins here:

#clear_nation()
#insert_db()

#print_csv()
#populate_db()

# Delete/Insertion query example
#clear_nation() # delete query - clear all data from nation relation
#populate_db() # insert/populate database with real data query (nation data only)
#access_db() # print all

# Selection+Update queries example 
#select_country_time("Andorra", "2022-08-05")
#update_db("Andorra", "2022-08-05", "n_confirmedcases", 0)
#select_country_time("Andorra", "2022-08-05")


# Selection example #2
#select_country_all("Andorra") # get all data of a country
