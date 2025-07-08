import requests

class CloudflareLLMClient:
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_solution_advice(self, task_text: str) -> str:
        payload = {
            "prompt": f"Объясни, как решать задачу:\n{task_text}",
            "max_tokens": 500,
            # Добавь другие параметры, если нужно
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            advice = data.get('choices', [{}])[0].get('text', '')
            return advice.strip()
        except requests.RequestException as e:
            print(f"Ошибка при запросе к Cloudflare LLM API: {e}")
            return ""
