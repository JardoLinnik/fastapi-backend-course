from schemas import TaskCreate, Task
from cloudflare_llm_client import CloudflareLLMClient
import os
import cloud_task_storage

API_KEY = os.getenv("CLOUDFLARE_API_KEY")
LLM_ENDPOINT = os.getenv("CLOUDFLARE_LLM_ENDPOINT")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID")
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")

llm_client = CloudflareLLMClient(api_key=API_KEY, endpoint=LLM_ENDPOINT)

storage = cloud_task_storage.CloudTaskStorage(bin_id=JSONBIN_BIN_ID, api_key=JSONBIN_API_KEY)

def get_tasks() -> list[Task]:
    return storage.get_tasks()

def create_task(task_data: TaskCreate) -> Task:
    try:
        advice = llm_client.get_solution_advice(task_data.title)
        full_text = f"{task_data.title}\n\nСоветы по решению:\n{advice}"
    except Exception as e:
        print(f"Ошибка при вызове LLM: {e}")
        full_text = task_data.title

    new_task_data = TaskCreate(title=full_text, status=task_data.status)
    return storage.create_task(new_task_data)

def update_task(task_id: int, task_data: TaskCreate) -> Task | None:
    return storage.update_task(task_id, task_data)

def delete_task(task_id: int) -> bool:
    return storage.delete_task(task_id)
