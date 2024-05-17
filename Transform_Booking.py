import pandas as pd
import numpy as np
from Fetch_Booking import Booking_fetch_data

def Transform_Booking():
    df_booking = Booking_fetch_data()
    
    df_booking = df_booking[df_booking['activity_activityName'] == 'การเรียนการสอน']
    df_booking[['semester', 'subjectCode', 'section']] = df_booking['remarks'].str.split('|', expand=True)
    columns_to_keep = [
        'subjectCode','section', 'room','activity-activityName', 
        'bookingStartDate', 'bookingEndDate'
    ]
    df_booking_filtered = df_booking[columns_to_keep]
    return df_booking_filtered
