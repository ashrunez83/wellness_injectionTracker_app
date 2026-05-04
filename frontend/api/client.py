import requests
import os 

# -------------------------------
# BASE URL (single source of truth)
# -------------------------------
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


# -------------------------------
# API HELPERS
# -------------------------------
def api_get(endpoint, params=None, default=None):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return default if default is not None else []


def api_post(endpoint, payload):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        return response, response.json()
    except Exception as e:
        return None, {"error": str(e)}


def api_put(endpoint, payload):
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", json=payload)
        return response, response.json()
    except Exception as e:
        return None, {"error": str(e)}


def api_delete(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}")
        return response, response.json()
    except Exception as e:
        return None, {"error": str(e)}