import sys
import traceback
import logging

logging.basicConfig(filename='backend.log', level=logging.INFO)

try:
    logging.info("Starting main.py...")
    from fastapi import FastAPI, Depends, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    logging.info("FastAPI imported")
    from database import get_db_connection, init_db
    logging.info("Database imported")
    from models import Shift
    logging.info("Models imported")
    from auth import get_current_username
    logging.info("Auth imported")
    import uuid
    from datetime import date
    import uvicorn

    app = FastAPI()

    # CORS configuration
    origins = [
        "http://localhost:5173",  # Vue dev server
        "http://localhost:3000",
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def read_root():
        return {"status": "online", "message": "Holiday Shift System Backend is running"}

    @app.on_event("startup")
    def startup_event():
        logging.info("Startup event triggered")
        try:
            init_db()
            logging.info("Database initialized")
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            logging.error(traceback.format_exc())

    @app.get("/debug")
    def debug_info():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT current_catalog()")
            current_catalog = cursor.fetchone()[0]
            
            cursor.execute("SELECT current_schema()")
            current_schema = cursor.fetchone()[0]
            
            cursor.execute("SHOW CATALOGS")
            catalogs = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            return {
                "current_catalog": current_catalog,
                "current_schema": current_schema,
                "catalogs": catalogs
            }
        except Exception as e:
            logging.error(f"Debug error: {e}")
            return {"error": str(e)}

    @app.get("/shifts")
    def get_shifts():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, collaborator_name, registration_number, holiday_date, created_at FROM main.default.holiday_shifts_v4")
            rows = cursor.fetchall()
            conn.close()
            
            shifts = []
            for row in rows:
                shifts.append({
                    "id": row.id,
                    "name": row.name,
                    "collaborator_name": row.collaborator_name,
                    "registration_number": row.registration_number,
                    "holiday_date": row.holiday_date,
                    "created_at": str(row.created_at)
                })
            return shifts
        except Exception as e:
            logging.error(f"Error in get_shifts: {e}")
            logging.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/shifts", dependencies=[Depends(get_current_username)])
    def create_shift(shift: Shift):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            shift_id = str(uuid.uuid4())
            import datetime
            current_time = datetime.datetime.now()
            cursor.execute(
                "INSERT INTO main.default.holiday_shifts_v4 (id, name, collaborator_name, registration_number, holiday_date, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (shift_id, shift.name, shift.collaborator_name, shift.registration_number, shift.holiday_date, current_time)
            )
            conn.close()
            return {"id": shift_id, "created_at": current_time, **shift.dict()}
        except Exception as e:
            logging.error(f"Error in create_shift: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/shifts/{shift_id}", dependencies=[Depends(get_current_username)])
    def delete_shift(shift_id: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM main.default.holiday_shifts_v4 WHERE id = ?", (shift_id,))
            conn.close()
            return {"message": "Shift deleted"}
        except Exception as e:
            logging.error(f"Error in delete_shift: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    if __name__ == "__main__":
        try:
            logging.info("Running uvicorn...")
            uvicorn.run(app, host="127.0.0.1", port=8080)
        except Exception as e:
            logging.error(f"Uvicorn crashed: {e}")
            logging.error(traceback.format_exc())

except Exception as e:
    logging.error(f"CRITICAL ERROR: {e}")
    logging.error(traceback.format_exc())
