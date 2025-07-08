import json
from typing import List, Optional
from schemas import Task, TaskCreate
import threading

class TaskStorage:
    def __init__(self, filename: str):
        self.filename = filename
        self.lock = threading.Lock()  # для избежания состояния гонки при работе с файлом
        self.tasks: List[Task] = []
        self.next_id = 1
        self._load()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task(**item) for item in data]
                if self.tasks:
                    self.next_id = max(task.id for task in self.tasks) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            self.next_id = 1

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in self.tasks], f, ensure_ascii=False, indent=4)

    def get_tasks(self) -> List[Task]:
        with self.lock:
            return self.tasks.copy()

    def create_task(self, task_data: TaskCreate) -> Task:
        with self.lock:
            task = Task(id=self.next_id, title=task_data.title, status=task_data.status)
            self.tasks.append(task)
            self.next_id += 1
            self._save()
            return task

    def update_task(self, task_id: int, task_data: TaskCreate) -> Optional[Task]:
        with self.lock:
            for idx, task in enumerate(self.tasks):
                if task.id == task_id:
                    updated_task = Task(id=task_id, title=task_data.title, status=task_data.status)
                    self.tasks[idx] = updated_task
                    self._save()
                    return updated_task
            return None

    def delete_task(self, task_id: int) -> bool:
        with self.lock:
            for idx, task in enumerate(self.tasks):
                if task.id == task_id:
                    del self.tasks[idx]
                    self._save()
                    return True
            return False
