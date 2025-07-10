from typing import List, Optional
from schemas import Task, TaskCreate
from base_http_client import BaseHTTPClient

class CloudTaskStorage(BaseHTTPClient):
    def __init__(self, bin_id: str, api_key: str):
        base_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        super().__init__(api_key, base_url)
        self.bin_id = bin_id

    def _load_tasks(self) -> List[Task]:
        data = self._request("GET", self.base_url + "/latest")
        if data is None:
            return []
        tasks_data = data.get('record', [])
        return [Task(**item) for item in tasks_data]

    def _save_tasks(self, tasks: List[Task]):
        tasks_dict = [task.dict() for task in tasks]
        response = self._request("PUT", self.base_url, json=tasks_dict)
        if response is None:
            raise Exception("Ошибка при сохранении задач")

    def get_tasks(self) -> List[Task]:
        return self._load_tasks()

    def create_task(self, task_data: TaskCreate) -> Task:
        tasks = self._load_tasks()
        next_id = max((task.id for task in tasks), default=0) + 1
        new_task = Task(id=next_id, title=task_data.title, status=task_data.status)
        tasks.append(new_task)
        self._save_tasks(tasks)
        return new_task

    def update_task(self, task_id: int, task_data: TaskCreate) -> Optional[Task]:
        tasks = self._load_tasks()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                updated_task = Task(id=task_id, title=task_data.title, status=task_data.status)
                tasks[i] = updated_task
                self._save_tasks(tasks)
                return updated_task
        return None

    def delete_task(self, task_id: int) -> bool:
        tasks = self._load_tasks()
        filtered_tasks = [task for task in tasks if task.id != task_id]
        if len(filtered_tasks) == len(tasks):
            return False
        self._save_tasks(filtered_tasks)
        return True
