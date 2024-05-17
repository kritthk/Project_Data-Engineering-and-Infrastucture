import pandas as pd
import numpy as np
from Fetch_Booking import Booking_fetch_data

def Transform_Booking():
    df_booking = Booking_fetch_data()
    df_booking[['semester', 'subjectCode', 'section']] = df_booking['remarks'].str.split('|', expand=True)
    df_booking.drop(columns=['remarks'], inplace=True)
    
    return df_booking

