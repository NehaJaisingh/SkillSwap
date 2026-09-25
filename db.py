import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="skillswap_user",
        password=os.getenv("SKILLSWAP_DB_PASSWORD"),
        database="skillswap_db"
    )