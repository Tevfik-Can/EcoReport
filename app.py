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


def insertreports(data):
    # Example data to insert to SQL
    db.insertreport(data)


def getreports():
    return db.getreport()


def makemap(result):
    gradient_colors = {
        0.2: '#ffff00',
        0.4: '#ffcc99',
        0.6: '#ff9966',
        0.8: '#ff0000',
        1.0: '#990000'
    }

    m = folium.Map(location=[45.425063550000004, -75.69991745871616], zoom_start=50)

    # # Example data (replace after)
    # report_loc = [
    #     [getLoc.latitude, getLoc.longitude],
    #     [34.0522, -118.2437],  # Los Angeles, CA
    #     [40.7128, -74.0060],  # New York, NY
    #     # Add more data points as needed
    # ]

    report_loc = []
    # Setting up the marker clusters
    marker_cluster = MarkerCluster().add_to(m)
    for entry in result:
        html = f"""
                <h1> {entry[2]}</h1>
                <p>You can use any html here! Let's do a list:</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
                </p>
                <p>And that's a <a href="https://python-graph-gallery.com">link</a></p>
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


app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123451231@localhost/db'
# db = SQLAlchemy(app)


@app.route('/')
def index():
    m = makemap(result=getreports())
    m.get_root().render()

    header = m.get_root().header.render()

    body_html = m.get_root().html.render()

    script = m.get_root().script.render()
    return render_template('index_page.html', header=header, body_html=body_html,
                           script=script)


@app.route('/crime_reported.html', methods=['GET', 'POST'])
def inserttodb():
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
            # data = {
            #     "report_name": request.form["report_name"],
            #     "category": request.form["category"],
            #     "coordinates": [getLoc.latitude, getLoc.longitude],  # Example latitude and longitude for New York City
            #     "date": datetime.strptime('2022-01-15', '%Y-%m-%d'),
            #     "addr": getLoc.address,
            #     # Fetch these variables with API
            #     "air_quality": "Good",
            #     "pollen_cond": "Low",
            #     "uv_index": "Quiet",
            # }

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
                "Quiet"
                "Moderate",
                None
            )
            insertreports(data)
            output = "Your report has been added to our database successfully!"

    else:
        output = "There was an error inserting the report into our database."
    m = makemap(result=getreports())
    m.get_root().render()

    header = m.get_root().header.render()

    body_html = m.get_root().html.render()

    script = m.get_root().script.render()
    return render_template('crime_reported.html', header=header, body_html=body_html, script=script, output=output)


if __name__ == "__main__":
    app.run(debug=True)
