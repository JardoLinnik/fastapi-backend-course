from typing import List, Optional
from schemas import Task, TaskCreate

tasks: List[Task] = []
next_id = 1

def get_tasks() -> List[Task]:
    return tasks

def create_task(task_data: TaskCreate) -> Task:
    global next_id
    task = Task(id=next_id, title=task_data.title, status=task_data.status)
    next_id += 1
    tasks.append(task)
    return task

def update_task(task_id: int, task_data: TaskCreate) -> Optional[Task]:
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(id=task_id, title=task_data.title, status=task_data.status)
            tasks[idx] = updated_task
            return updated_task
    return None

def delete_task(task_id: int) -> bool:
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[idx]
            return True
    return False
