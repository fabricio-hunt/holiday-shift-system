from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(filename='test_server.log', level=logging.INFO)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    try:
        logging.info("Starting test server...")
        uvicorn.run(app, host="127.0.0.1", port=8080, loop="asyncio")
        logging.info("Server stopped.")
    except Exception as e:
        logging.error(f"Server crashed: {e}")
