import pandas as pd
from Fetch_Temp import Temp_fetch_data

def Transform_Booking():
    df = Temp_fetch_data()
    df = df.rename(columns={'Heat': 'Fahrenheit', 'Temp': 'Celsius'})
    return df