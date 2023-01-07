# Monkeypox Global Data Visualizer
Group #18
12/4/2022
Alexander Ono

To run the entire application:
    python3 pyqt5.py
    
(must have PostgreSQL running with database name as 'finalproject' - see `sql_creation_queries` file to see queries used to build database and run the function `populate_db()` in `sql_script.py` to populate the database with the CDC covid data from the csv file)

To run the webpage component only, run with command in UNIX terminal (requires npm live-server):
    live-server

Raw data was provided by OWID:

https://github.com/owid/monkeypox

# Video Demo: 

https://youtu.be/Pp8j2Qmg0_I


# Dependencies:
    pycountry-convert

install dependency with:

    pip3 install pycountry-convert
