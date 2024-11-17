
import pandas as pd
import mysql.connector
from mysql.connector import Error

try:
    # Attempt to connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",       # Change if your MySQL server is remote
        user="root",    # Replace with your MySQL username
        password="root",# Replace with your MySQL password
        database="fort_database"
    )
    if conn.is_connected():
        print("Connected to MySQL database")
    
    cursor = conn.cursor()

    # Load CSV data
    df = pd.read_csv("with_lat_lon/fort_details.csv")
    print("Data loaded from CSV:")
    print(df.head())

    # Insert data
    for index, row in df.iterrows():
        try:
            sql = """
            INSERT INTO fort_details (district, fort_name, lat, lon, link)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (row["district"], row["fort_name"], row["lat"], row["lon"], row["link"]))
            print(f"Inserted row {index+1}: {row.values}")
            
            if (index + 1) % 10 == 0:
                conn.commit()

        except Exception as e:
            print(f"Error inserting row {index+1}: {e}")

    conn.commit()
    print("Data insertion completed and committed.")

except Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")


