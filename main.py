from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def get_status():
    return {"status": "online", "message": "Server is running!"}

@app.get("/data")
def get_data():
    return {"id": 1, "info": "This is the smallest possible backend."}
