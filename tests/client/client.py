import asyncio
import websockets
import json


class Client:
    def __init__(
        self,
        base_url: str,
        master_token: str | None = None,
        access_token: str | None = None,
    ):
        self.master_token: str = master_token
        self.access_token: str = access_token
        self.base_url: str = base_url

        self.__headers: dict | None = None

    @property
    def headers(self) -> dict:
        if self.__headers is not None:
            return self.__headers

        headers: dict = {}
        if self.master_token is not None:
            headers["MASTER-TOKEN"] = self.master_token
        if self.access_token is not None:
            headers["ACCESS-TOKEN"] = self.access_token

        self.__headers = headers
        return headers

    async def open_ws(self, path: str):
        url = f"{self.base_url}{path}"
        async with websockets.connect(
            url,
            additional_headers=self.headers,
            ping_interval=0,
        ) as websocket:
            connection = await websocket.recv()
            connection = json.loads(connection)
            accepted: bool = connection["status"] == "success"
            print(("✅" if accepted else "❌") + f" {connection['detail']}\n")

            while accepted:
                mensaje = input(">> ")
                await websocket.send(mensaje)

                try:
                    recived_message = await websocket.recv()
                    print(f"<< {recived_message}")
                except asyncio.TimeoutError:
                    pass
