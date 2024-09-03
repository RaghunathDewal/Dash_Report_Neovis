from psycopg2 import pool
import polars as pl
from DB.db import DB

try:
    DB.initialize()
except Exception as init_err:
    print(f"Error initializing database: {init_err}")
    raise

def Task():
    query = """SELECT a.id, a.task_title, a.task_description, a.task_type, a.status, 
                      b.property_name AS location, a.organization_id
               FROM task a
               LEFT JOIN property b ON a.property_id = b.id;"""
    df1,query_err = DB.execute_query(query)
    if query_err:
        print(f"Error executing query: {query_err}")
        return
    
    
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
    df2,query_err =  DB.execute_query(query)
    if query_err:
        print(f"Error executing query: {query_err}")
        return
    
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


