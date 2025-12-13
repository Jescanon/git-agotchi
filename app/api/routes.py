import httpx

TIMEOUT_SECONDS = 10

async def get_inf_user(name):
    name = name.lower().strip()

    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        response = await client.get(f"https://api.github.com/users/{name}")

    if response.status_code == 404:
        return False

    if response.status_code == 200:
        data = response.json()
        return data.get("login")

async def get_inf_events(name):
    try:
        name = name.lower().strip()

        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.get(f"https://api.github.com/users/{name}/events")
        if response.status_code == 404:
            return False

        if response.status_code == 200:
            return response.json()
    except:
        return False