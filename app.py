# ADD CREATE EVENT + JOIN EVENT WHERE USER PUTS IN THE REPORT ID THEY WANT TO REGISTER OR CREATE
# DYNAMICALLY CLOSE BUTTONS IF THERE IS ALREADY AN EVENT MADE FOR THAT

# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim

# importing folium and its plugin Heatmap
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

# To insert date parameter in SQL
from datetime import datetime

# import sql file
import addressesdb as db

# import flask for creating website
from flask import Flask, render_template, request


# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def insertreports(data):
    # Example data to insert to SQL
    db.insertreport(data)


def getreports():
    return db.getreport()


def makemap(result, start_lat, start_long):
    gradient_colors = {
        0.2: '#ffff00',
        0.4: '#ffcc99',
        0.6: '#ff9966',
        0.8: '#ff0000',
        1.0: '#990000'
    }
    if start_long == 0 and start_lat == 0:
        m = folium.Map(location=[45.425063550000004, -75.69991745871616], zoom_start=30)
    else:
        m = folium.Map(location=[start_lat, start_long], zoom_start=30)

    # # Example data (replace after)
    # report_loc = [
    #     [getLoc.latitude, getLoc.longitude],
    #     [34.0522, -118.2437],  # Los Angeles, CA
    #     [40.7128, -74.0060],  # New York, NY
    #     # Add more data points as needed
    # ]

    report_loc = []
    # Setting up the marker clusters
    # marker_cluster = MarkerCluster().add_to(m)

    for entry in result:
        print(entry)
        if entry[11] is None:
            html = f"""
                    <h1> {entry[2]}</h1>
                    <p>Address: {entry[6]}</p>
                    <div>               
                    Create an Event!
                    </div>
                    """
        else:
            eventdetails = db.geteventbyid(id=entry[11])
            html = f"""
                    <h1> {entry[2]}</h1>
                    <p>Address: {entry[6]}</p>
                    <div>
                    <p>Event Organized by: {eventdetails[2]}</p>
                    <p>Date: {eventdetails[3]}</p>
                    <p>People that joined so far: {eventdetails[4]}</p>
                    </div>
                    <div>
                    <span class="text">
                    Join the Event!
                    </span>
                    </div>
                    """
        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=1650)

        # Gathering the reports for Heatmap
        report_loc.append([entry[4], entry[3]])
        # Marker customizations
        folium.Marker(
            location=[entry[4], entry[3]],
            # popup=entry[1],
            icon=folium.Icon(icon="seedling", prefix='fa', color="green"),
            # # icon taken from https://fontawesome.com/icons/categories/humanitarian
            popup=popup
        ).add_to(m)

    HeatMap(report_loc, min_opacity=0.3, blur=25, gradient=gradient_colors).add_to(m)
    return m


def inserttoeventdb():
    reportid = 1
    event_data = {
        'John Doe',
        datetime.strptime('2022-01-15', '%Y-%m-%d'),
        reportid
    }
    db.insertevent(data=event_data, reportid=reportid)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123451231@localhost/db'
# db = SQLAlchemy(app)


@app.route('/')
def index():
    m = makemap(result=getreports(), start_lat=0, start_long=0)
    m.get_root().render()

    header = m.get_root().header.render()

    body_html = m.get_root().html.render()

    script = m.get_root().script.render()

    reports = getreports()
    ids = []
    for e in reports:
        ids.append(e[0])
    return render_template('index_page.html', header=header, body_html=body_html,
                           script=script, ids=ids)


@app.route('/crime_reported.html', methods=['GET', 'POST'])
def inserttodb():
    start_lat = 0
    start_long = 0
    if request.method == 'POST':

        # calling the Nominatim tool and create Nominatim class
        loc = Nominatim(user_agent="Geopy Library")

        # ADD ERROR HANDLILNG FOR UNRECOGNIZED ADDRESSES
        # entering the location name
        getLoc = loc.geocode(request.form['location'])
        if getLoc.address is None:
            print("The address cannot be found")
        else:
            # printing address
            print(getLoc.address)

            # printing latitude and longitude
            print("Latitude = ", getLoc.latitude, "\n")
            print("Longitude = ", getLoc.longitude)
            # Example data to insert to SQL
            data = (
                request.form["report_name"],
                request.form["category"],
                getLoc.latitude,
                getLoc.longitude,
                datetime.strptime('2022-01-15', '%Y-%m-%d'),
                getLoc.address,
                # Fetch these variables with API
                "Good",
                "Low",
                "Quiet",
                "Moderate"
            )
            insertreports(data)
            output = "Your report has been added to our database successfully!"
            start_lat = getLoc.latitude
            start_long = getLoc.longitude
    else:
        output = "There was an error inserting the report into our database."
    m = makemap(result=getreports(), start_lat=start_lat, start_long=start_long)
    m.get_root().render()

    header = m.get_root().header.render()

    body_html = m.get_root().html.render()

    script = m.get_root().script.render()
    return render_template('crime_reported.html', header=header, body_html=body_html, script=script, output=output)


if __name__ == "__main__":
    app.run(debug=True)
