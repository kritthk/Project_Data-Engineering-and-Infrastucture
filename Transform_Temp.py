import pandas as pd
from Fetch_Temp import Temp_fetch_data

def Transform_Booking():
    df_temp = Temp_fetch_data()
    df_temp = df_temp.rename(columns={'Temp': 'Celsius'})
    df_temp.drop(columns=['Humidity','Heat'], inplace=True)
    return df_temp