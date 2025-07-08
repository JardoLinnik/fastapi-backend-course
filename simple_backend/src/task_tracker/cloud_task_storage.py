import requests
from typing import List, Optional
from schemas import Task, TaskCreate

class CloudTaskStorage:
    def __init__(self, bin_id: str, api_key: str):
        self.bin_id = bin_id
        self.api_key = api_key
        self.base_url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"
        self.headers = {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _load_tasks(self) -> List[Task]:
        try:
            response = requests.get(self.base_url + "/latest", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            tasks_data = data.get('record', [])
            return [Task(**item) for item in tasks_data]
        except requests.RequestException as e:
            print(f"Ошибка при загрузке задач: {e}")
            return []

    def _save_tasks(self, tasks: List[Task]):
        tasks_dict = [task.dict() for task in tasks]
        try:
            response = requests.put(self.base_url, headers=self.headers, json=tasks_dict)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при сохранении задач: {e}")
            raise

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
