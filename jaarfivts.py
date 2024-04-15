"""
My take on the vts class
"""

from pyvts.error import AuthenticationError
import websockets
import models
import json
from pathlib import Path
import aiofiles
import aiofiles.os
import platformdirs

APPNAME = "JaarfiVts"
APPAUTHOR = "Jaarfi"
TOKEN_DIR = platformdirs.user_data_path(APPNAME, APPAUTHOR)
TOKEN_FILE = TOKEN_DIR / "token.txt"


class Token:
    def __init__(self, path):
        self.path = Path(path)
        self.token = None

    async def save(self) -> None:
        if self.token is None:
            raise ValueError("Token not set")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self.path, mode="w") as f_token:
            await f_token.write(self.token)

    async def load(self) -> str:
        async with aiofiles.open(self.path, mode="r") as f_token:
            self.token = await f_token.read()
            assert self.token != ""
            return self.token

    async def delete(self) -> str:
        await aiofiles.os.remove(self.path)


class JaarfiVts:
    """
    ``VtubeStudio API`` Connector

    Args
    ----------
    plugin_info : dict of {"plugin_name", "developer", "plugin_icon", "authentication_token_path"}

        Information about your plugin.

    vts_api_info: dict of {"version", "name", "port"}
        Informatiopn about VtubeStudio API.

    """

    def __init__(self, port: int = 8001, token_path=TOKEN_FILE) -> None:
        self.port = port
        self.websocket = None
        self.auth_token = Token(token_path)
        self.connected = False

    async def connect(self) -> None:
        """Connect to VtubeStudio API server"""
        try:
            self.websocket = await websockets.connect(f"ws://localhost:{self.port}")
            self.connected = True

        except ConnectionError as e:
            print("Error: ", e)
            print("Please ensure VTubeStudio is running and")
            print("the API is running on ws://localhost:", str(self.port))

    async def close(self) -> None:
        """
        Close connection
        """
        await self.websocket.close(code=1000, reason="user closed")
        self.connected = False

    async def request(self, request_msg: models.BaseRequest) -> dict:
        """
        Send request to VTubeStudio

        Args
        ----------
        request_msg : requests_vts.BaseRequest
            A generic Request

        Returns
        -------
        response_dict
            Message from VTubeStudio API, data is stored in ``return_dict["data"]``
        """
        await self.websocket.send(request_msg.model_dump_json(by_alias=True))
        response_msg = await self.websocket.recv()
        response_dict = json.loads(response_msg)
        return response_dict

    async def make_authentication_token_request(
        self, request_msg: models.AuthenticationTokenRequest
    ) -> str:
        """Get authentication token from VTubeStudio"""
        response = await self.request(request_msg)
        if "authenticationToken" in response["data"]:
            return response["data"]["authenticationToken"]
        else:
            raise AuthenticationError(response["data"]["message"])

    async def make_authentication_request(
        self, request_msg: models.AuthenticationRequest
    ):
        """Get authenticated for one session"""
        response = await self.request(request_msg)
        if not response["data"]["authenticated"]:
            await self.auth_token.delete()
            raise AuthenticationError(response["data"]["reason"])

    async def authenticate(
        self, authentication_token_request: models.AuthenticationTokenRequest
    ):
        try:
            await self.auth_token.load()
        except:
            self.auth_token.token = await self.make_authentication_token_request(
                authentication_token_request
            )
            await self.auth_token.save()
        await self.make_authentication_request(
            models.AuthenticationRequest(
                data=models.AuthenticationData(
                    plugin_name=authentication_token_request.data.plugin_name,
                    plugin_developer=authentication_token_request.data.plugin_developer,
                    authentication_token=self.auth_token.token,
                )
            )
        )
