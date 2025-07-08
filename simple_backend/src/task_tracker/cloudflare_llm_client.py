from typing import Optional
from base_http_client import BaseHTTPClient

class CloudflareLLMClient(BaseHTTPClient):
    def __init__(self, api_key: str, endpoint: str):
        super().__init__(api_key, endpoint)

    def get_tasks(self):
        raise NotImplementedError("Метод get_tasks не поддерживается для LLM клиента")

    def create_task(self, task_data):
        raise NotImplementedError("Метод create_task не поддерживается для LLM клиента")

    def update_task(self, task_id: int, task_data):
        raise NotImplementedError("Метод update_task не поддерживается для LLM клиента")

    def delete_task(self, task_id: int) -> bool:
        raise NotImplementedError("Метод delete_task не поддерживается для LLM клиента")

    def get_solution_advice(self, task_text: str) -> str:
        payload = {
            "prompt": f"Объясни, как решать задачу:\n{task_text}",
            "max_tokens": 500,
        }
        data = self._request("POST", self.base_url, json=payload)
        if data is None:
            return ""
        advice = data.get('choices', [{}])[0].get('text', '')
        return advice.strip()
