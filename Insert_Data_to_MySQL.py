import pymysql.cursors

from Attendance_fetch_data import Attendance_fetch_data
from Booking_fetch_data import Booking_fetch_data

def establish_connection():
    try:
        connection = pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         password='1234',
                                         db='project')
        return connection
    except pymysql.Error as e:
        print("Error connecting to MySQL:", e)

def insert_data_to_mysql(data, table_name, connection):
    try:
        cursor = connection.cursor()
        data_str = data.astype(str)
        for index, row in data_str.iterrows():
            columns = ', '.join(data_str.columns)
            placeholders = ', '.join(['%s'] * len(data_str.columns))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(row))
            connection.commit()
        print("Data inserted to "+ table_name +" successfully.")
    except pymysql.Error as e:
        print("Error inserting data:", e)
    finally:
        cursor.close()


if __name__ == "__main__":
    attendance_data = Attendance_fetch_data()
    booking_data = Booking_fetch_data()

    connection = establish_connection()

    if connection:
        if attendance_data is not None:
            insert_data_to_mysql(attendance_data, "attendance",connection)
        if booking_data is not None:
            insert_data_to_mysql(booking_data, "booking",connection)
        connection.close()
