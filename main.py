from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
app = FastAPI()

# set up localhost 3000 with uvicorn
# uvicorn main:app --reload http://localhost:3000
# run uvicorn in terminal
# basic end point from stage

      
# ====================={ stage 0 run simple hello server }=========================
# ---- Existing endpoints ----
@app.get("/status")
def get_status():
    return {"status": "online", "message": "Server is running!"}

@app.get("/data")
def get_data():
    return {"id": 1, "info": "This is the smallest possible backend."}


# ====================={ stage 1 Your first real end_point }=======================

# point 1
@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

# point 2   
@app.get("/health")
def get_health():
    return {"status":"OK"}   

#======================{ stage 2 Read: list and single task }=======================

# point 1:  -- create a tasks 3 list 
tasks = [{"id":0, "title":"this is a FIRST normal task in the backend","done":False},
        {"id":1, "title":"this is a SECOND normal task in the backend","done":True},
        {"id":2, "title":"this is a THIRD normal task in the backend","done":False}
        ]

# point 2: get all tasks 
@app.get("/tasks")
def get_tasks():
    return tasks  

# point 3 & 4 combined: get single task and return error if not found
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    if task_id not in [task["id"] for task in tasks]:
        return {"status":"404","message":f"Task_ID {task_id} not found"}
        # raise HTTPException(status_code=404, detail="Task_ID not found") # 2nd way
    return tasks[task_id]

#======================{ stage 3 POST: add new task }=======================

# ---- Input model: only "title" is expected from the client ----
class TaskCreate(BaseModel):
    title: str = " "

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # Next free id = highest existing id + 1 (works even if tasks are deleted later)
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "400", "message": "Title is required and cannot be empty"}
        )

    next_id = int(max((task["id"] for task in tasks), default=-1)) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)

    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks

#======================{ stage 4 UPDATE and DELETE tasks }=======================

    
