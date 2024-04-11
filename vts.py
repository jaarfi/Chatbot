import asyncio, pyvts
import os.path
import time

class vtsconn:

    def __init__(self, myvts: pyvts.vts):
        self.myvts = myvts

    async def connect_auth(self):
        await self.myvts.connect()
        if not os.path.exists('./authentication_token.txt'):
            await self.myvts.request_authenticate_token()  # get token
            with open('./authentication_token.txt', 'w') as file:
                file.write(self.myvts.authentic_token)
        
        with open('./authentication_token.txt') as file:
            self.myvts.authentic_token = file.read()
        await self.myvts.request_authenticate()  # use token
        await self.myvts.close()

    async def flip(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        
        steps = 30
        for i in range(steps):
            await self.myvts.request(
                self.myvts.vts_request.requestMoveModel(0,0,size=0,rot=int(360/steps), relative=True, move_time=0))
        await self.myvts.close()

    async def reset(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0,0,size=-70,rot=0, relative=False, move_time=1))
        await self.myvts.close()

    async def slideright(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0.3,0,size=0, relative=True, move_time=1))
        await self.myvts.close()

    async def zoomin(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0,0,size=10, relative=True, move_time=1))
        await self.myvts.close()

    async def getItems(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemList(False, True, False))
        print(response)
        await self.myvts.close()

    async def toggleHeadpat(self, seconds: int):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=1))
        time.sleep(seconds)
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=0))
        await self.myvts.close()

    async def turboHeadpat(self, seconds: int):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=1, framerate=60))
        time.sleep(seconds)
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=0))
        await self.myvts.close()

    async def zoomMoustache(self):
        print("hello")
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemMove('93dd087fedcd44dda640fa72e13c6bd5',positionX=0.1,rotation=90, size=0.5))
        print(response)
        await self.myvts.close()

    async def pixel(self, pixelation: int, strength: float):
        print("hello")
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestPixelation(strength, pixelation))
        print(response)
        await self.myvts.close()