from fastapi import FastAPI

app = FastAPI()

# set up localhost 3000 with uvicorn
# uvicorn main:app --reload http://localhost:3000
# run uvicorn in terminal
# basic end point from stage

#----- { stage 2 Read: list and single task } ------------

# point 1:
tasks = [{"id":0, "title":"this is a FIRST normal task in the backend","done":False},
        {"id":1, "title":"this is a SECOND normal task in the backend","done":True},
        {"id":2, "title":"this is a THIRD normal task in the backend","done":False}
        ]

# point 2:
@app.get("/tasks")
def get_tasks():
    return tasks  

# point 3 & 4 combined:
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    if task_id not in [task["id"] for task in tasks]:
        return {"status": "404"}
    return tasks[task_id]

      

# ----           { stage 0 run simple hello server }
@app.get("/status")
def get_status():
    return {"status": "online", "message": "Server is running!"}

@app.get("/data")
def get_data():
    return {"id": 1, "info": "This is the smallest possible backend."}


# { stage 1 Your first real end_point }

# point 1
@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

# point 2   
@app.get("/health")
def get_health():
    return {"status":"OK"}   


