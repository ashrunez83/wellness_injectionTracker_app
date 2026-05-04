import requests
import os 

# -------------------------------
# BASE URL (single source of truth)
# -------------------------------
BASE_URL = os.getenv("API_BASE_URL")

if not BASE_URL:
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "")
    if render_hostname == "orelia-app.onrender.com":
        BASE_URL = "https://wellness-injectiontracker-app.onrender.com"
    else:
        BASE_URL = "http://127.0.0.1:8000"

BASE_URL = BASE_URL.rstrip("/")
API_URL = BASE_URL


def _response_error(response):
    body = response.text.strip()
    if response.status_code == 403:
        return (
            f"API request was forbidden by {BASE_URL}. "
            "Check the frontend service API_BASE_URL setting in Render."
        )
    return body or f"API returned status {response.status_code} with an empty response"


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
        try:
            return response, response.json()
        except ValueError:
            return response, {"error": _response_error(response)}
    except Exception as e:
        return None, {"error": str(e)}


def api_put(endpoint, payload):
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", json=payload)
        try:
            return response, response.json()
        except ValueError:
            return response, {"error": _response_error(response)}
    except Exception as e:
        return None, {"error": str(e)}


def api_delete(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}")
        try:
            return response, response.json()
        except ValueError:
            return response, {"error": _response_error(response)}
    except Exception as e:
        return None, {"error": str(e)}
