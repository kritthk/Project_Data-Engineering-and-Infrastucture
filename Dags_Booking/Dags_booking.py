import json
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# 7YTzkxTT8n7i2FEMX7eS67Ba+BnN2PtUZTSazeiUFX4=
import json
import requests
import urllib.parse
from datetime import datetime
import pandas as pd

default_args = {
    'owner': 'Your name',
    'start_date': datetime(2024, 1, 24),
}

def post_data_to_api():
    # Prepare the data payload
    data = {
        'apiKey': "7YTzkxTT8n7i2FEMX7eS67Ba+BnN2PtUZTSazeiUFX4=",
        'version': 1
    }
    data['apiKey'] = urllib.parse.quote_plus(data['apiKey'])

    # Format the URL with the version from the data
    url = f'https://de.ict.mahidol.ac.th/data-service/v{data['version']}/Authen/apikey?apiKey={data['apiKey']}'

    # Headers for the POST request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request with data payload
    response = requests.post(url, headers=headers)

    response_json = response.json()
    status_code = response_json.get('statusCode')
    if(status_code >= 400 or status_code != 200):
        return f'Failed to post data. Status code: {status_code}, Response: {response.text}'
    else:
        data_object = response_json.get("data")
        return data_object.get('token')

def get_data_api_booking(**kwargs):
    token = kwargs['task_instance'].xcom_pull(task_ids='post_data_task')
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    if not token:
        return "token not found"
    data = {
        'startDate': "2023-04-20",
        'endDate': f"{formatted_date}",
        'room': "IT 105",
        'floor': "1",
        'version': "1"
    }

    full_url = f'https://de.ict.mahidol.ac.th/data-service/v{data['version']}/Booking/FetchData'

    if data:
        full_url += "?" + "&".join([f"{key}={value}" for key, value in data.items()])
    headers = {
        'Content-Type': 'text/plain',
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(full_url, headers=headers, json=data)
    response_json = response.json()
    status_code = response_json.get('statusCode')
    if(status_code >= 400 or status_code != 200):
        return f'Failed to post data. Status code: {status_code}, Response: {response.text}'
    else:
        data_str = json.dumps(response_json.get('data'))
        data_json = json.loads(data_str)
        return data_json

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def save_data_to_database(**kwargs):
    data = kwargs['task_instance'].xcom_pull(task_ids='get_data_task')
    if not data:
        return "No data available to save"

    # Connect to the database
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = postgres_hook.get_conn()

    # Create INSERT INTO query
    with conn.cursor() as cursor:
        for item in data:
            for participant in item['participants']:  # Iterate over participants directly
                cursor.execute("""
                    INSERT INTO mahidol_booking (bookingId, activityId, bookingRequestDate, bookingStartTime, bookingEndTime, durationInMinute, remarks, activity_activityId, activity_activityName, bookingEndDate, bookingStartDate, requesterName, room, floor, participants_participantTypeId, participants_participantType, participants_amountExact, participants_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    item['bookingId'], item['activityId'], item['bookingRequestDate'], item['bookingStartTime'], item['bookingEndTime'], item['durationInMinute'], item['remarks'], item['activity']['activityId'], item['activity']['activityName'], item['bookingEndDate'], item['bookingStartDate'], item['requesterName'], item['room'], item['floor'], participant['participantTypeId'], participant['participantType'], participant['amountExact'], participant['amount']
                ))

    conn.commit()




def create_table_if_not_exists():
    # สร้างคำสั่งสร้างตาราง
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS mahidol_booking (
            bookingId INTEGER,
            activityId INTEGER,
            bookingRequestDate TIMESTAMP,
            bookingStartTime VARCHAR,
            bookingEndTime VARCHAR,
            durationInMinute INTEGER,
            remarks VARCHAR,
            activity_activityId INTEGER,
            activity_activityName VARCHAR,
            bookingEndDate DATE,
            bookingStartDate DATE,
            requesterName VARCHAR,
            room VARCHAR,
            floor INTEGER,
            participants_participantTypeId VARCHAR,
            participants_participantType VARCHAR,
            participants_amountExact VARCHAR,
            participants_amount VARCHAR
        );
    """

    # เชื่อมต่อฐานข้อมูล
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = postgres_hook.get_conn()

    # สร้างตาราง
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

with DAG('mahidol_booking',
         schedule_interval='@daily',
         default_args=default_args,
         description='A DAG for posting and fetching data from an API mahidol booking',
         catchup=False) as dag:

    post_data_task = PythonOperator(
        task_id='post_data_task',
        python_callable=post_data_to_api,
        provide_context=True
    )

    get_data_task = PythonOperator(
        task_id='get_data_task',
        python_callable=get_data_api_booking,
        provide_context=True
    )

    create_table_data_task = PythonOperator(
        task_id='create_table_data_task',
        python_callable=create_table_if_not_exists,
        provide_context=True
    )

    save_data_task = PythonOperator(
        task_id='save_data_task',
        python_callable=save_data_to_database
    )

    post_data_task >> get_data_task >> create_table_data_task >> save_data_task