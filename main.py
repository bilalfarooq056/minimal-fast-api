from fastapi import FastAPI, HTTPException,status,Query
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_connection
from contextlib import asynccontextmanager
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # code here runs on startup
    init_db()
    yield
    # code here would run on shutdown (nothing needed for us)

app = FastAPI(lifespan=lifespan)



# +++++++++++++++++++++++++++
#         A1 Week_2             
# +++++++++++++++++++++++++++
# set up localhost 3000 with uvicorn
# uvicorn main:app --reload http://localhost:3000
# run uvicorn in terminal
# basic end point from stage



      
# ====================={ stage 0 Create your database }=========================
# ---- Exrta And optional Task----
@app.get("/stats")
def get_stats():
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    pending_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 0").fetchone()[0]

    conn.close()

    return {
        "total": total,
        "done": done_count,
        "pending": pending_count
    }

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

#======================{ stage 2 Read from the database  }=======================

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

#======================{ stage 3 - Create new tasks }=======================

# ---- Input model: only "title" is expected from the client ----
class TaskCreate(BaseModel):
    title: str = " "

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # Next free id = highest existing id + 1 (works even if tasks are deleted later)
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required" )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )
    conn.commit()

    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()

    return dict(row)

@app.get("/tasks")
def get_tasks():
    return tasks

#======================{ stage 3 & 4 Update and delete & Learn your first SQL }=======================
# point 1 
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done:  Optional[bool] = None


class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    conn = get_connection()
    cursor = conn.cursor()

    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ?, updated_at = datetime('now') WHERE id = ?",
        (task.title, int(task.done), task_id)
    )
    conn.commit()

    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return dict(row)


# point 2 
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return None


# -----> Publish your database project
# ==================== Optional extras=====================

@app.get("/tasks")
def get_tasks(
    search: Optional[str] = Query(None),
    done: Optional[bool] = Query(None),
    sort: Optional[str] = Query(None)
):
    conn = get_connection()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if done is not None:
        query += " AND done = ?"
        params.append(int(done))

    if sort == "title":
        query += " ORDER BY title ASC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in rows]

