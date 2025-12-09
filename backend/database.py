from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN"),
        catalog="main",
        schema="default"
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create table if not exists
    try:
        cursor.execute("DROP TABLE IF EXISTS main.default.holiday_shifts_v4")
    except Exception as e:
        print(f"Error dropping table: {e}")
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS main.default.holiday_shifts_v4 (
            id STRING,
            name STRING,
            collaborator_name STRING,
            registration_number STRING,
            holiday_date DATE,
            created_at TIMESTAMP
        ) USING DELTA
    """)
    conn.close()
