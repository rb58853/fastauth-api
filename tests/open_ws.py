from client.client import Client
import asyncio

client: Client = Client(
    base_url="ws://localhost:8000/test-api",
    master_token="kAONxbkATfyk3kmnUhw7YyAMotmvuJ6tVsuT1w3A6N4=",
    access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJlOTMyMzcwNi0zNzY3LTRmZGQtYjU5MS04ZmMxZmRlNzk4MzAiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4ODE4ODA0LCJpYXQiOjE3NTYyMjY4MDR9.0dzPRm2u1wL7wKTgsMGpOVPFa_GpjnSr826cxEVOiaI",
)

asyncio.run(client.open_ws(path="/ws/master"))
asyncio.run(client.open_ws(path="/ws/access"))
