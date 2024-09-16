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
    df1, query_err = DB.execute_query(query)
    if query_err:
        print(f"Error executing query: {query_err}")
        return

    if df1 is not None:
        df1 = df1.rename(
            {
                "id": "ID",
                "task_title": "Task",
                "task_description": "Description",
                "task_type": "Type",
                "status": "Status",
                "location": "Location",
                "organization_id": "ORG",
            }
        )
        return df1


def Time():
    query = """SELECT a.id, a.task_title, a.task_description, a.task_type, a.status, 
                      a.assigned_at, a.completed_at, a.start_time, 
                      A.time_diff AS completion_time, 
                      a.start_time - a.end_time AS calc_completion_time, 
                      b.property_name AS location, a.organization_id
               FROM task a
               LEFT JOIN property b ON a.property_id = b.id;"""
    df2, query_err = DB.execute_query(query)
    if query_err:
        print(f"Error executing query: {query_err}")
        return

    if df2 is not None:
        df2 = df2.rename(
            {
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
                "organization_id": "ORG",
            }
        )
        return df2


def get_employee_date():
    query = '''select CONCAT(
        UPPER(SUBSTRING(u.first_name FROM 1 FOR 1)), 
        LOWER(SUBSTRING(first_name FROM 2)), 
        ' ', 
        UPPER(SUBSTRING(u.last_name FROM 1 FOR 1)), 
        LOWER(SUBSTRING(u.last_name FROM 2))
        ) AS Employee_name,t.id as task_id,t.task_title ,t.task_description  ,t.time_spent,ti.inspection_comment,ti.inspection_rating,p.property_name,t.organization_id 
        from task t left join "user" u 
        on t.assigned_to_id = u.id
        left  join property p  on t.property_id=p.id
        left join task_inspection ti on t.id=ti.task_id;'''
    df3, query_err = DB.execute_query(query)
    if query_err:
        print(f"Error executing query: {query_err}")
        return
    if df3 is not None:
        df3 = df3.rename(
            {
                "Employee_name": "Employee_name",
                "task_id": "Task_ID",
                "task_title": "Task_Title",
                "task_description": "Summary",
                "time_spent": "Time_Spent",
                "inspection_comment": "Comments",
                "inspection_rating": "Rating",
                "property_name": "Location",
                "organization_id": "ORG",
            }
        )
        df3 = df3.sort("Task_ID",descending=True)  
        return df3
