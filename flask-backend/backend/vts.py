import os.path
import time
import pyvts

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

    async def flip(self, steps: int):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        for i in range(steps):
            response = await self.myvts.request(
                self.myvts.vts_request.requestMoveModel(0,0,size=0,rot=int(360/steps), relative=True, move_time=0))
        await self.myvts.close()
        return response
    
    async def spin(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        
        steps = 2
        response = await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0,0,size=0,rot=179, relative=True, move_time=2)) #spinining 
        response = await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0,0.2,size=0,rot=0, relative=True, move_time=2)) #moving around
        await self.myvts.close()
        return response

    async def reset(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0,0,size=-75,rot=0, relative=False, move_time=1))
        await self.myvts.close()

    async def slideright(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        await self.myvts.request(
            self.myvts.vts_request.requestMoveModel(0.3,0,size=0, relative=True, move_time=1))
        await self.myvts.close()
        return ""

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

    async def pat(self, seconds: int):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=1, framerate=17))
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

    async def pixel(self, pixelation: int):
        print("hello")
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestPixelation(1, pixelation))
        time.sleep(5)
        response = await self.myvts.request(
            self.myvts.vts_request.requestPixelation(1, 1,postProcessingOn=False))
        await self.myvts.close()
        print(response)
        return response
    
    async def getHotkeys(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestHotKeyList())
        print(response)
        await self.myvts.close()

    async def hearteyes(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("9fdbf0f8d333465ab82e81c186a8c535"))
        print(response)
        await self.myvts.close()

    async def glasses(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("d9ec03db2ffd4b918623918bf5c963ea"))
        print(response)
        await self.myvts.close()

    async def sunglasses(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("e2eda84a04e34f019ee0ebd7c6545837"))
        print(response)
        await self.myvts.close()

    async def disableAll(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("aaa15614bb71434db9b2b3664483872b"))
        print(response)
        await self.myvts.close()

    async def blush(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("1db1e2ce1d0045a1ac6347904f688b0f"))
        print(response)
        await self.myvts.close()
        return ""
    
    async def sparkles(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("341d6ce18a2f45bf8b74ef3378d3b5f6"))
        print(response)
        await self.myvts.close()
        return ""
    
    async def angy(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey("ff5db1762f7a45028f57a8a06c6395a9"))
        print(response)
        await self.myvts.close()
        return ""
    
    async def expression(self, name):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestHotKeyList())
        avail = response['data']['availableHotkeys']
        id = next(item for item in avail if item["name"] == name)['hotkeyID']
        response = await self.myvts.request(
            self.myvts.vts_request.requestTriggerHotKey(id))
        print(response)
        await self.myvts.close()
        return ""
    
    async def expressions(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate()
        response = await self.myvts.request(
            self.myvts.vts_request.requestHotKeyList())
        avail = response['data']['availableHotkeys']
        id = "available expressions: "
        b = (item['name'] + " " for item in avail)

        return id+''.join(b)