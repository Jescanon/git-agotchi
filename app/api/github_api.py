import httpx
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request

from .routes import get_inf_events

router = APIRouter(tags=["api"], prefix="/api")

TIMEOUT_SECONDS = 100


async def get_code_inf(name):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(f"https://api.github.com/repos/{name}")

        if response.status_code == 404:
            return False

        if response.status_code == 200:
            return await parse_github_commit_json(response.json())
    except:
        return False


async def parse_github_commit_json(commit_data: dict) -> str:
    files = commit_data.get("files", [])

    result_text = ""

    for file in files:
        filename = file.get("filename")
        patch = file.get("patch")
        status = file.get("status")

        if not patch:
            continue

        if filename.endswith(('.png', '.jpg', '.svg', '.json')):
            continue

        result_text += f"File: {filename} ({status})\n"
        result_text += patch
        result_text += "\n\n"

    return result_text

@router.get("/{name}")
async def root(name: str, request: Request, info: dict = Depends(get_inf_events)):
    if not info:
        return f"Произошла ошибка, попробуйте еще раз"

    inf_ab_headers = request.headers.get("APIS", None)
    flag = False
    if inf_ab_headers:
        flag = True

    s = []
    for i in info:
        m = i.get("type", None)
        time_now = datetime.now().replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(i.get("created_at"))
        if m and m == "PushEvent" and i.get("actor").get("login").lower() == name.lower():
            info_time = {
                "interval": ((time_now - dt).total_seconds()) // 86400,
                "time": dt,
                "name_directory": i.get("repo").get("name"),
                "SHA": i.get("payload").get("head") if type(i.get("payload")) is dict else None
            }
            s.append(info_time)

    if not flag:
        information = s.copy()[0]
        result = await get_code_inf(f"{information.get('name_directory')}/commits/{information.get('SHA')}")
        return result

    return s

async def get_request(name, headeres: bool | None = None):
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        if headeres:
            headers = {
                "APIS": "YES"
            }
            response = await client.get(f"http://127.0.0.1:8000/api/{name}", headers=headers)
        else:
            response = await client.get(f"http://127.0.0.1:8000/api/{name}")

    if response.status_code == 404:
        return False

    return response.json()