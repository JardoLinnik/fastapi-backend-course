import requests
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseHTTPClient(ABC):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при запросе {method} {url}: {e}")
            return None

    @abstractmethod
    def get_tasks(self) -> List[Any]:
        pass

    @abstractmethod
    def create_task(self, task_data: Any) -> Any:
        pass

    @abstractmethod
    def update_task(self, task_id: int, task_data: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        pass
