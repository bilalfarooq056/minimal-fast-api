from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_connection
app = FastAPI()


# +++++++++++++++++++++++++++
#         A1 Week_2             
# +++++++++++++++++++++++++++
# set up localhost 3000 with uvicorn
# uvicorn main:app --reload http://localhost:3000
# run uvicorn in terminal
# basic end point from stage

@app.on_event("startup")
def startup():
    init_db()


      
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
tasks = [{"id":0, "title":"Your FIRST Order Is Here","done":False},
        {"id":1, "title":"Your SECOND Order Is Here","done":True},
        {"id":2, "title":"Your THIRD Order Is Here","done":False}
        ]

# point 2: get all tasks 
@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return [dict(row) for row in rows]  

# point 3 & 4 combined: get single task and return error if not found
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail = "Task not found")

    return dict(row)

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

    next_id = int(max((task["id"] for task in tasks), default=-1)) + 1 # this works even if the center value is missed
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)

    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks

#======================{ stage 4 UPDATE and DELETE tasks }=======================
# point 1 
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done:  Optional[bool] = None


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):

    # find the task
    task = next((t for t in tasks if t["id"]== task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # validate: at least one field must be provided
    if update.title is None and update.done is None:
        raise HTTPException(status_code=400, detail="Provideat least 'title' or 'done' to update")

    #validate: if title is given, it can't be empty
    if update.title is not None and not update.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    
    # apply only field that were sent
    if update.title is not None:
        task["title"] = update.title
    if update.done is not None:
        task["done"] = update.done

    return task 




# point 2 
# -----> removes the task. Return status 204 ("No Content" — success, nothing to say) with an empty body.  
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in [task["id"] for task in tasks]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "404", "message": f"Task_ID {task_id} not found"}
        )
    del tasks[task_id]
    return {"status": "success", "message": f"Task {task_id} deleted successfully - nothing to say"}

'''
# Extras: 
#  curl -i http://localhost:3000/tasks?search=milk
#  curl -i http://localhost:3000/tasks?done=true

> out:1
HTTP/1.1 200 OK
date: Thu, 16 Jul 2026 17:39:39 GMT
server: uvicorn
content-length: 172
content-type: application/json

[{"id":0,"title":"Your FIRST Order Is Here","done":false},{"id":1,"title":"Your SECOND Order Is Here","done":true},{"id":2,"title":"Your THIRD Order Is Here","done":false}](venv)

> out:2
#  HTTP/1.1 200 OK
# date: Thu, 16 Jul 2026 17:37:15 GMT
# server: uvicorn
# content-length: 172
# content-type: application/json

# [{"id":0,"title":"Your FIRST Order Is Here","done":false},{"id":1,"title":"Your SECOND Order Is Here","done":true},{"id":2,"title":"Your THIRD Order Is Here","done":false}](venv)
'''





# =============================================================================================================
# +++++++++++++++++++++++++++
#         A2 Week_2             
# +++++++++++++++++++++++++++




