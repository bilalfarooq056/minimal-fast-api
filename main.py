from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to the smallest backend!"}

@app.get("/status")
def get_status():
    return {"status": "online", "message": "Server is running!"}

@app.get("/data")
def get_data():
    return {"id": 1, "info": "This is the smallest possible backend."}

@app.get("/health")
def get_health():
    return {"status": "OK"}    


