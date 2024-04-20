import os.path
import time
import pyvts
import jaarfivts.models as models


class vtsconn:

    def __init__(self, myvts: pyvts.vts):
        self.myvts = myvts

    async def connect_auth(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate_token(
            models.AuthenticationTokenRequest()
        )  # get token
        await self.myvts.close()

    async def flip(self, steps: int):
        if steps.isdigit():
            steps = int(steps)
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        for i in range(steps):
            response = await self.myvts.request(
                self.myvts.vts_request.requestMoveModel(
                    0, 0, size=0, rot=int(360 / steps), relative=True, move_time=0
                )
            )
        await self.myvts.close()
        return "response"

    async def spin(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()

        steps = 2
        response = await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(
                0, 0, size=0, rot=179, relative=True, move_time=2
            )
        )  # spinining
        response = await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(
                0, 0.2, size=0, rot=0, relative=True, move_time=2
            )
        )  # moving around
        await self.myvts.close()
        return "response"

    async def reset(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(
                0, 0, size=-75, rot=0, relative=False, move_time=1
            )
        )
        await self.myvts.close()

    async def slideright(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(
                0.3, 0, size=0, relative=True, move_time=1
            )
        )
        await self.myvts.close()
        return ""

    async def zoomin(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(
                0, 0, size=10, relative=True, move_time=1
            )
        )
        await self.myvts.close()

    async def getItems(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemList(False, True, False)
        )
        print(response)
        await self.myvts.close()

    async def pat(self, seconds: str):
        if seconds.isdigit():
            seconds = float(seconds)
        else:
            return "only accepts int"
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl(
                "b5a7e8ba1c0b42eda2460328618da2cb", opacity=1, framerate=17
            )
        )
        print(response)
        time.sleep(seconds)
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl(
                "b5a7e8ba1c0b42eda2460328618da2cb", opacity=0
            )
        )
        print(response)
        await self.myvts.close()

    async def turboHeadpat(self, seconds: str):
        if seconds.isdigit():
            seconds = float(seconds)
        else:
            return "only accepts int"
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl(
                "b5a7e8ba1c0b42eda2460328618da2cb", opacity=1, framerate=60
            )
        )
        time.sleep(seconds)
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl(
                "b5a7e8ba1c0b42eda2460328618da2cb", opacity=0
            )
        )
        await self.myvts.close()

    async def zoomMoustache(self):
        print("hello")
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemMove(
                "93dd087fedcd44dda640fa72e13c6bd5", positionX=0.1, rotation=90, size=0.5
            )
        )
        print(response)
        await self.myvts.close()

    async def pixel(self, pixelation: int):
        print("hello")
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestPixelation(1, pixelation)
        )
        time.sleep(5)
        response = await self.myvts.request(
            self.myvts.vts_request.requestPixelation(1, 1, postProcessingOn=False)
        )
        await self.myvts.close()
        print(response)
        return ""

    async def getHotkeys(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(self.myvts.vts_request.requestHotKeyList())
        print(response)
        await self.myvts.close()

    async def expression(self, name):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(self.myvts.vts_request.requestHotKeyList())
        avail = response["data"]["availableHotkeys"]
        id = next(item for item in avail if item["name"] == name)["hotkeyID"]
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey(id)
        )
        print(response)
        await self.myvts.close()
        return ""

    async def expressions(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(self.myvts.vts_request.requestHotKeyList())
        avail = response["data"]["availableHotkeys"]
        id = "available expressions: "
        b = (item["name"] + " " for item in avail)

        return id + "".join(b)
