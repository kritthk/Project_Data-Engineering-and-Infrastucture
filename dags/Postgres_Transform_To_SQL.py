import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

def Save_Data_Tran_func(data,table_name):
    # Convert data back to DataFrame
    df = pd.DataFrame(data)
    
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    engine = postgres_hook.get_sqlalchemy_engine()
    
    # Save the DataFrame to the PostgreSQL database
    df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi')

    return print("Saved Data temperature to database successfully.")