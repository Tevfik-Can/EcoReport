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
                   "air_quality, pollen_cond, noise_pol, uv_index) VALUES" \
                   "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

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
