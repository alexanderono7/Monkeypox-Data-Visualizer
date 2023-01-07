# Monkeypox Global Data Visualizer

A PostreSQL application for visualizing MonkeyPox data on a three-dimensional global heatmap.

[VIDEO DEMO](https://youtu.be/Pp8j2Qmg0_I)

### UI Controls
-Drag globe view around with click & hold

-Zoom In/Out with scroll wheel

-Adjust the slider to change the current date (and update the map correspondingly - and yes this actually queries the database and doesn't just use the csv file)

-Move cursor over a country to view its current value of interest (you can't see my cursor in the screenshots but you can see the tooltip that pops up in the 2nd and 3rd pictures) 

-Use the radio buttons to change the statistic type you're querying for


To run the entire application:
    
    python3 pyqt5.py
    
(must have PostgreSQL running with database name as 'finalproject' - see `sql_creation_queries` file to see queries used to build database and run the function `populate_db()` in `sql_script.py` to populate the database with the CDC covid data from the csv file)

To run the webpage component only, run with command in UNIX terminal (requires npm live-server):
    live-server

[Raw data was provided by OWID](https://github.com/owid/monkeypox)

# Dependencies:
    pycountry-convert

install dependency with:

    pip3 install pycountry-convert
