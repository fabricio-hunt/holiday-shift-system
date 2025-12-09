from database import init_db
import logging
import traceback

logging.basicConfig(level=logging.INFO)

try:
    print("Initializing database...")
    init_db()
    print("Database initialized successfully.")
except Exception as e:
    print(f"Database initialization failed: {e}")
    traceback.print_exc()
