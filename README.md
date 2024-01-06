# Eco Report
This application is a reporting app for enviromentally bad crimes or helping others such as picking up trash, helping homeless etc.

# How the Application Works
## Server Side
The server is responsible for handling incoming reports from clients and displaying the report in the map for all other clients. When the client wants to report a crime, the server will take its geo location and other related content into an SQL database for use.
Event making will be added later on, where after a crime has been reported others can create an event to resolve the issue or participate on an already created event.
Also the basic statistics such as air pollution will be added later on whenever a new report has been added for data analysis.

![image](https://github.com/Tevfik-Can/EcoReport/assets/74112509/241648da-34d7-4b34-9215-34e8d502daa7)


## Client Side
The clients will be taken to the web browser where they can see all the on going reports, with that information they can include their own report or join an event that was created for a report.

![image](https://github.com/Tevfik-Can/EcoReport/assets/74112509/34b03ca7-0281-4576-ac9c-fee1338cafaf)

## Running the Application
First, link your sql database credentials to [ addressesdb.py ] and create the databases
Second, run the app.py file in cmd using [ python app.py ] in the location of the file to start the server.
Next, connect to the loopback address with port 5000 [ http://127.0.0.1:5000/ ] in your web brtowser. The application will take you to the index page.

![image](https://github.com/Tevfik-Can/EcoReport/assets/74112509/451cb330-d127-449c-b293-bad9d0acc3f5)

# What I've Learned
Through this project, I've learned the following key concepts:

### SQL Programming:
How to connect to mysql databases and insert or gather information from them.
### Python Flask:
How to create and display a working website from python using flask with a pleasing UI.
### Folium Graph GUI: 
How to implement a folium map into an html file.
### HTML and CSS: 
Refreshed my mind on HTML and CSS by creating and decorating a form in the website

# Future improvements
- Event Create / Join
- Include Weather Conditions, Air pollution etc into the report sql
- Proper date and time for reports and events
- After a data has been passed, take the report down
- Make another table for completed reports
- Display only completed reports
