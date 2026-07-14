from fastapi import FastAPI

app = FastAPI()

# set up localhost 3000 with uvicorn
# uvicorn main:app --reload http://localhost:3000
# run uvicorn in terminal
# basic end point from stage


# ----           { stage 0 run simple hello server }
@app.get("/status")
def get_status():
    return {"status": "online", "message": "Server is running!"}

@app.get("/data")
def get_data():
    return {"id": 1, "info": "This is the smallest possible backend."}


# stage 1

# point 1
@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
    
@app.get("/health")
def get_health():
    return {"status":"OK"}   


