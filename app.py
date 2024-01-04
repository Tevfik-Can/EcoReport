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
# calling the Nominatim tool and create Nominatim class
loc = Nominatim(user_agent="Geopy Library")

# ADD ERROR HANDLILNG FOR UNRECOGNIZED ADDRESSES
# entering the location name
getLoc = loc.geocode("280 Forestbrook st")

# printing address
print(getLoc.address)

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)

# # Example data to insert to SQL
# data = (
#     "A lot of trash",
#     "Clean up",
#     getLoc.latitude,  getLoc.longitude,  # Example latitude and longitude for New York City
#     datetime.strptime('2022-01-15', '%Y-%m-%d'),
#     "123 Main St, City, Country",
#     "Good",
#     "Low",
#     "Quiet",
#     "Moderate"
# )
# db.insertreport(data)
#
# result = db.getreport()
# print(result[0])
# m = folium.Map(location=[getLoc.latitude, getLoc.longitude], zoom_start=50)

m = folium.Map(location=[45.34410185, -75.9370470146851], zoom_start=50)

# -------- Heat Map Customizations
# Example data (replace after)
report_loc = [
    [getLoc.latitude, getLoc.longitude],
    [34.0522, -118.2437],  # Los Angeles, CA
    [40.7128, -74.0060],  # New York, NY
    # Add more data points as needed
]


# Custom gradient colours (replace after)
gradient_colors = {
    0.2: '#ffff00',
    0.4: '#ffcc99',
    0.6: '#ff9966',
    0.8: '#ff0000',
    1.0: '#990000'
}
#
# # Gathering the reports for Heatmap
# report_loc = []
# for entry in result:
#     report_loc.append([entry[4], entry[3]])
#
# # Setting up the marker clusters
# marker_cluster = MarkerCluster().add_to(m)
# for entry in result:
#     # Marker customizations
#     folium.Marker(
#         location=[entry[4], entry[3]],
#         popup=entry[1],
#         icon=folium.Icon(icon="seedling", prefix='fa', color="green"),
#         # icon taken from https://fontawesome.com/icons/categories/humanitarian
#     ).add_to(marker_cluster)
#
HeatMap(report_loc, min_opacity=0.3, blur=25, gradient=gradient_colors).add_to(m)



from flask import Flask, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123451231@localhost/db'
# db = SQLAlchemy(app)


@app.route('/')
def index():
    m.get_root().render()

    header = m.get_root().header.render()

    body_html = m.get_root().html.render()

    script = m.get_root().script.render()
    return render_template('index_page.html', header=header, body_html=body_html, script=script)


if __name__ == "__main__":
    app.run(debug=True)
