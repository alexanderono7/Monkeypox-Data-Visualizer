from collections import defaultdict
import pycountry_convert as pc
import pycountry
import psycopg2
import subprocess
import csv
import os

header = ['location', 'iso_code', 'date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'new_cases_smoothed', 'new_deaths_smoothed', 'new_cases_per_million', 'total_cases_per_million', 'new_cases_smoothed_per_million', 'new_deaths_per_million', 'total_deaths_per_million', 'new_deaths_smoothed_per_million']

# Creating dictionary of alpha2 -> alpha3 country codes
alpha_codes = dict()
for country in list(pycountry.countries):
    alpha_codes[country.alpha_2] = country.alpha_3

# Given the alpha 2 ISO code of a country, return its corresponding alpha 3 ISO code
def getAlpha3(alpha2:str) -> str:
    return alpha_codes[alpha2]

# Given the alpha 2 ISO code of a country, return its continent
def country_to_continent(country_alpha2:str) -> str:
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

# Parse monkeypox data csv file
def print_csv():
    with open('owid-monkeypox-data.csv', newline='') as csvfile:
        monkey_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i,row in enumerate(monkey_reader):
            if i is not 0:
                print(' | '.join(row))
    print(header)

# Read out all tuples from 'nation' relation
def access_db():
    conn = psycopg2.connect(dbname='db412project')
    cur = conn.cursor()
    cur.execute('select * from nation')
    for x in cur:
        print(x)
    #print(dir(cur))
    #print(type(cur))
    cur.close()
    conn.close()

# insert dummy row into nation relation
def insert_db():
    conn = psycopg2.connect(dbname='db412project')
    cur = conn.cursor()

    nationkey = 13
    nationname = "dummyname"
    conf_cases = 4
    conf_deaths = 7
    new_cases = 4
    new_deaths = 2
    n_contkey = 4

    insert_query = f'''
    INSERT INTO nation (N_NATIONKEY, N_NAME, N_CONFIRMEDCASES, N_CONFIRMEDDEATHS, N_NEWCASES, N_NEWDEATHS, N_CONTKEY) 
    VALUES ({nationkey}, \'{nationname}\', {conf_cases}, {conf_deaths}, {new_cases}, {new_deaths}, {n_contkey});
    '''
    cur.execute(insert_query)
    conn.commit()
    cur.close()
    conn.close()

# remove all rows from 'nation' relation
def clear_nation():
    conn = psycopg2.connect(dbname='db412project')
    cur = conn.cursor()
    delete_query = f'''
    DELETE FROM nation;
    '''
    cur.execute(delete_query)
    conn.commit()
    cur.close()
    conn.close()

# Populate db with csv data
def populate_db():
    conn = psycopg2.connect(dbname='db412project')
    cur = conn.cursor()
    with open('owid-monkeypox-data.csv', newline='') as csvfile:
        monkey_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i,row in enumerate(monkey_reader):
            if i is not 0:
                #nationkey = int(''.join([str(ord(x)) for x in row[1]]))
                nationkey = i
                nationname = row[0]
                conf_cases = row[3]
                conf_deaths = row[4]
                new_cases = row[5]
                new_deaths = row[6]
                n_contkey = 4 # temp value
                date = str("\'" + row[2] + "\'")
                insert_query = f'''
                INSERT INTO nation (N_NATIONKEY, N_NAME, N_CONFIRMEDCASES, N_CONFIRMEDDEATHS, N_NEWCASES, N_NEWDEATHS, N_CONTKEY, date) 
                VALUES ({nationkey}, \'{nationname}\', {conf_cases}, {conf_deaths}, {new_cases}, {new_deaths}, {n_contkey}, {date});
                '''
                cur.execute(insert_query)
    conn.commit()
    cur.close()
    conn.close()

# Update a the data for a specific country at a specific instance in time
def update_db(nkey, date, attr, value):
    conn = psycopg2.connect(dbname='db412project')
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
    conn = psycopg2.connect(dbname='db412project')
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
    conn = psycopg2.connect(dbname='db412project')
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

subprocess.run('clear')
# Presentation/Demo begins here:

#clear_nation()
#insert_db()
print_csv()

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
