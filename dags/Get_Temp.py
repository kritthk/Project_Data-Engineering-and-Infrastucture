from datetime import datetime, timedelta
import pandas as pd

def Get_Temp():
    csv_file = '/opt/airflow/dags/data/data.csv'
    current_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df = df[df['Date'] <= current_time] 
    return df
