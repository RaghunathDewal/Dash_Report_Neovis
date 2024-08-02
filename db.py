import psycopg2
from psycopg2 import pool
import time
import polars as pl
import os
from dotenv import load_dotenv
load_dotenv()
postgres_url = os.getenv('DB_URL')


connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=postgres_url)

def connect_and_fetch_data(query):
    df = None
    try:
        
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
 
        # start_time = time.time()
        
     
        cursor.execute(query)
        
        data = cursor.fetchall()
        
     
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print(f"Time taken to fetch data: {elapsed_time} seconds")

        
        column_names = [desc[0] for desc in cursor.description]
        df = pl.DataFrame(data, schema=column_names, orient="row", strict=False)
        
        cursor.close()
        connection_pool.putconn(conn)
        
    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")
    return df

def Task():
    query = """SELECT a.id, a.task_title, a.task_description, a.task_type, a.status, 
                      b.property_name AS location, a.organization_id
               FROM task a
               LEFT JOIN property b ON a.property_id = b.id;"""
    df1 = connect_and_fetch_data(query)
    if df1 is not None:
        df1 = df1.rename({
            "id": "ID",
            "task_title": "Task",
            "task_description": "Description",
            "task_type": "Type",
            "status": "Status",
            "location": "Location",
            "organization_id": "ORG"
        })
        return df1

def Time():
    query = """SELECT a.id, a.task_title, a.task_description, a.task_type, a.status, 
                      a.assigned_at, a.completed_at, a.start_time, 
                      A.time_diff AS completion_time, 
                      a.start_time - a.end_time AS calc_completion_time, 
                      b.property_name AS location, a.organization_id
               FROM task a
               LEFT JOIN property b ON a.property_id = b.id;"""
    df2 = connect_and_fetch_data(query)
    
    if df2 is not None:
        df2 = df2.rename({
            "id": "ID",
            "task_title": "Task",
            "task_description": "Description",
            "task_type": "Type",
            "status": "Status",
            "assigned_at": "Assigned_at",
            "completed_at": "Completed_at",
            "start_time": "Start_time",
            "completion_time": "Completion_time",
            "calc_completion_time": "Calc_Completion_Time",
            "location": "Location",
            "organization_id": "ORG"
        })
        return df2

