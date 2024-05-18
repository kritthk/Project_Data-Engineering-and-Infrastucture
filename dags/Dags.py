import pandas as pd
import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


from Get_Token import Get_Api_Token
from Get_Booking import Get_Booking
from Get_Attendance import Get_Attendance
from Get_Temp import Get_Temp
from Transform_Temp import Transform_Temp
from Transform_Attendance import Transform_Attendance
from Transform_Booking import Transform_Booking
    
def Get_Booking_Data_Task(**kwargs):
    ti = kwargs['ti']
    api_token = ti.xcom_pull(task_ids='Get_Api_Token')
    if not api_token:
        raise ValueError("No API token retrieved.")
    return Get_Booking(api_token)
    
def Get_Attendance_Data_Task(**kwargs):
    ti = kwargs['ti']
    api_token = ti.xcom_pull(task_ids='Get_Api_Token')
    booking_data = ti.xcom_pull(task_ids='Get_Booking_Data')
    if not api_token:
        raise ValueError("No API token retrieved.")
    return Get_Attendance(api_token, booking_data)

def Transform_Attendance_Task(**kwargs):
    ti = kwargs['ti']
    attendance_data = ti.xcom_pull(task_ids='Get_Attendance_Data')
    return Transform_Attendance(attendance_data)

def Transform_Booking_Task(**kwargs):
    ti = kwargs['ti']
    booking_data = ti.xcom_pull(task_ids='Get_Booking_Data')
    return Transform_Booking(booking_data)

def Transform_Temp_Task(**kwargs):
    ti = kwargs['ti']
    temp_data = ti.xcom_pull(task_ids='Get_Temp_Data')
    return Transform_Temp(temp_data)

default_args = {
    'owner': 'Krit',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('Project',
         default_args=default_args,
         description='A DAG for posting and fetching data',
         schedule_interval=None,
         catchup=False) as dag:

    Get_Token = PythonOperator(
        task_id='Get_Api_Token',
        python_callable=Get_Api_Token,
        provide_context=True
    )

    Get_Booking_Data = PythonOperator(
        task_id='Get_Booking_Data',
        python_callable=Get_Booking_Data_Task,
        provide_context=True
    )

    Get_Attendance_Data = PythonOperator(
        task_id='Get_Attendance_Data',
        python_callable=Get_Attendance_Data_Task,
        provide_context=True
    )
    
    Transform_Attendance_Data = PythonOperator(
        task_id='Transform_Attendance_Data',
        python_callable=Transform_Attendance_Task,
        provide_context=True
    )
    
    Transform_Booking_Data = PythonOperator(
        task_id='Transform_Booking_Data',
        python_callable=Transform_Booking_Task,
        provide_context=True
    )
    
    Get_Temp_Data = PythonOperator(
        task_id='Get_Temp_Data',
        python_callable=Get_Temp,
        provide_context=True
    )
    
    Transform_Temp_Data = PythonOperator(
        task_id='Transform_Temp_Data',
        python_callable=Transform_Temp_Task,
        provide_context=True
    )
    

    Get_Token >> Get_Booking_Data >> Get_Attendance_Data >> Transform_Attendance_Data
    Get_Temp_Data >> Transform_Temp_Data
    Get_Booking_Data >> Transform_Booking_Data
