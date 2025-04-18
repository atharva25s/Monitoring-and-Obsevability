import uvicorn
from fastapi import FastAPI, HTTPException
import random
import time
import logging
from multiprocessing import Queue
from prometheus_fastapi_instrumentator import Instrumentator
import logging_loki

# Initialize FastAPI app
app = FastAPI()

# Prometheus Metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Loki Logging
log_queue = Queue(-1)  

loki_handler = logging_loki.LokiQueueHandler(
    log_queue,
    url="http://<LOKI_URL>/loki/api/v1/push",  # Change to your Loki URL
    tags={"application": "fastapi-emulator"},
    version="1"
)

# Setup Logger
logger = logging.getLogger("fastapi-emulator")
logger.setLevel(logging.INFO)
logger.addHandler(loki_handler)

# Uvicorn Access Logger
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addHandler(loki_handler)

# Endpoints
@app.get("/status")
def get_status():
    logger.info("GET /status - Service is running")
    return {"message": "Service is running"}

@app.get("/process")
def process_request():
    delay = random.choice([1, 2, 5, 10])  
    time.sleep(delay)
    logger.info(f"GET /process - Request took {delay} seconds")
    return {"message": "Request processed", "delay": delay}

@app.get("/unstable")
def unstable_api():
    if random.random() < 0.3:  
        logger.error("GET /unstable - Simulated failure")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    logger.info("GET /unstable - Request successful")
    return {"message": "Request succeeded"}

@app.get("/data/{item_id}")
def get_data(item_id: int):
    logger.info(f"GET /data/{item_id} - Returning data")
    return {"item_id": item_id, "value": f"Data for {item_id}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
