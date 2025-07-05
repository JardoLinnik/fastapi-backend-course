from fastapi import FastAPI, HTTPException
from typing import List
import crud
from schemas import Task, TaskCreate

app = FastAPI()

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return crud.get_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    return crud.create_task(task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    updated = crud.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = crud.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
