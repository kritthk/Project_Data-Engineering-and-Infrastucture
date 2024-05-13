from datetime import datetime, timedelta
import pandas as pd

def read_csv_to_df():
    csv_file = 'data.csv'
    current_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df = pd.read_csv(csv_file)
    df = df.rename(columns={'Heat': 'Fahrenheit', 'Temp': 'Celsius'})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df = df[df['Date'] <= current_time] 
    return df
