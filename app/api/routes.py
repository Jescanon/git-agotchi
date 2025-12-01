import httpx

response = httpx.request(method="GET",url="https://api.github.com/users/Jescanon/events")
print(response.text)