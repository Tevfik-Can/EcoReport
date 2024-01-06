import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123451231",
    database="ecoreports"
)

mycursor = mydb.cursor()


def insertreport(data):
    # SQL statement for insertion
    sqlstatement = "INSERT INTO reports (r_name, r_category, r_latitude, r_longitude, r_date, r_address, " \
                   "air_quality, pollen_cond, noise_pol, uv_index, event_id) VALUES" \
                   "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"

    try:
        # Execute the insertion
        mycursor.execute(sqlstatement, data)

        # Commit the changes
        mydb.commit()

        print("Record inserted successfully!")
    except mysql.connector.IntegrityError as e:
        if "unique_lat_long" in str(e):
            print("Error: Duplicate latitude and longitude. Record not inserted.")
        else:
            print(f"Error: {e}")


def getreport():
    mycursor.execute("SELECT * FROM reports")
    return mycursor.fetchall()


def insertevent(data, reportid):

    # Create the SQL INSERT statement
    insert_query = '''
        INSERT INTO events (e_organizer_name, e_date, report_id)
        VALUES (%s, %s, %s)
    '''

    try:
        # Execute the insertion
        mycursor.execute(insert_query, data)
        # Commit the changes
        mydb.commit()

        print("Record inserted successfully!")
        # Get the ID of the last inserted row in the events table
        last_event_id = mycursor.lastrowid

        update_report_query = '''
            UPDATE reports
            SET event_id = %s
            WHERE report_id = %s
        '''
        # Execute the query to update the report entry with the newly created event
        mycursor.execute(update_report_query, (last_event_id, reportid))
        mydb.commit()
    except mysql.connector.IntegrityError as e:
        print(f"Error: {e}")

def geteventbyid(id):
    sql_statement = "SELECT * FROM events WHERE event_id = %s"
    mycursor.execute(sql_statement, id)
    return mycursor.fetchone()
