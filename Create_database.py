import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': '3306',
}

database_name = 'project'

create_table_attendance = f"""
CREATE TABLE IF NOT EXISTS attendance (
    id INT,
    subjectCode VARCHAR(50),
    subjectName VARCHAR(255),
    sections INT,
    numEnrolledStd INT,
    numPresent FLOAT,
    percentPresent FLOAT,
    numAbsent FLOAT,
    percentAbsent FLOAT,
    numLeave FLOAT,
    percentLeave FLOAT,
    classDate DATE,
    classStart TIME,
    classEnd TIME
)
"""

create_table_booking = f"""
CREATE TABLE IF NOT EXISTS booking (
    bookingId INT PRIMARY KEY,
    activityId INT,
    bookingRequestDate DATETIME,
    bookingStartTime TIME,
    bookingEndTime TIME,
    durationInMinute INT,
    bookingEndDate DATE,
    bookingStartDate DATE,
    requesterName VARCHAR(255),
    room VARCHAR(50),
    floor INT,
    participants TEXT,
    activity_activityId INT,
    activity_activityName VARCHAR(255),
    semester INT,
    subjectCode VARCHAR(50),
    section INT
)
"""

create_table_temp = f"""
CREATE TABLE IF NOT EXISTS temp (
    Date DATE,
    Time TIME,
    celsius FLOAT,
    humidity FLOAT,
    fahrenheit FLOAT
)
"""

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' created successfully or already exists.")

    cursor.execute(f"USE {database_name}")
    
    cursor.execute(create_table_attendance)
    print(f"Table attendance created successfully or already exists.")
    
    cursor.execute(create_table_booking)
    print(f"Table booking created successfully or already exists.")
    
    cursor.execute(create_table_temp)
    print(f"Table temp created successfully or already exists.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor.close()
    cnx.close()
