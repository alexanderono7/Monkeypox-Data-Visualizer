CSE412 - Databases Final Project
Group #18
12/4/2022
Alexander Ono

https://youtu.be/Pp8j2Qmg0_I

MonkeyPox Global Data Visualizer

To run the entire application:
    python3 pyqt5.py
    
(must have PostgreSQL running with database name as 'finalproject' - see `sql_creation_queries` file to see queries used to build database and run the function `populate_db()` in `sql_script.py` to populate the database with the CDC covid data from the csv file)

Dependencies:
    pycountry-convert

install with:
    pip3 install pycountry-convert
   

To run the webpage component only, run with command in UNIX terminal (requires npm live-server):
    live-server

Raw data was provided by OWID:

https://github.com/owid/monkeypox
