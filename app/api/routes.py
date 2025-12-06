import httpx

TIMEOUT_SECONDS = 10

async def get_inf(name):
    name = name.lower().strip()

    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        response = await client.get(f"https://api.github.com/users/{name}")

    if response.status_code == 404:
        return False

    if response.status_code == 200:
        data = response.json()
        return data.get("login")
