import psycopg2
from psycopg2 import pool
import polars as pl
import os
from dotenv import load_dotenv

load_dotenv()


class DB:
    connection_pool = None

    @classmethod
    def initialize(cls):
        if cls.connection_pool is None:
            try:
                url = os.getenv("PROD_DB_URL")
                cls.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=url)
                print("Database connection pool initialized.")
            except Exception as e:
                print(f"Error initializing database connection pool: {e}")
                raise e

    @classmethod
    def execute_query(cls, query):
        if cls.connection_pool is None:
            return None, "Database not initialized"

        df = None
        try:
            conn = cls.connection_pool.getconn()
            if cls.is_connection_closed(conn):
                print("Connection was closed, getting a new one.")
                conn = cls.connection_pool.getconn()

            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            column_names = [desc[0] for desc in cursor.description]
            df = pl.DataFrame(
                data,
                schema=column_names,
                orient="row",
                strict=False,
                infer_schema_length=None,
            )
            

            cursor.close()
            cls.connection_pool.putconn(conn)

        except Exception as error:
            return None, f"Error executing query: {error}"
        return df, None

    @classmethod
    def close_connection_pool(cls):
        if cls.connection_pool:
            cls.connection_pool.closeall()
            cls.connection_pool = None

    @classmethod
    def is_connection_closed(cls, conn):
        return conn.closed != 0
