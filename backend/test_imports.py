print("Starting imports...")
try:
    import pydantic
    print("pydantic imported")
    import fastapi
    print("fastapi imported")
    import uvicorn
    print("uvicorn imported")
    import dotenv
    print("dotenv imported")
    import databricks.sql
    print("databricks.sql imported")
except Exception as e:
    print(f"Error: {e}")
