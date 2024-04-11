import asyncio, pyvts
import os.path
import time

async def connect_auth(myvts: pyvts.vts):
    await myvts.connect()
    if not os.path.exists('./authentication_token.txt'):
        await myvts.request_authenticate_token()  # get token
        with open('./authentication_token.txt', 'w') as file:
            file.write(myvts.authentic_token)
    
    with open('./authentication_token.txt') as file:
        myvts.authentic_token = file.read(myvts.authentic_token)
    await myvts.request_authenticate()  # use token
    await myvts.close()

async def flip(myvts: pyvts.vts):
    await myvts.connect()
    await myvts.request_authenticate()
    
    steps = 30
    for i in range(steps):
        await myvts.request(
            myvts.vts_request.requestMoveModel(0,0,size=0,rot=int(360/steps), relative=True, move_time=0))
    await myvts.close()

async def reset(myvts: pyvts.vts):
    await myvts.connect()
    await myvts.request_authenticate()
    await myvts.request(
        myvts.vts_request.requestMoveModel(0,0,size=-70,rot=0, relative=False, move_time=1))
    await myvts.close()

async def slideright(myvts: pyvts.vts):
    await myvts.connect()
    await myvts.request_authenticate()
    await myvts.request(
        myvts.vts_request.requestMoveModel(0.3,0,size=0, relative=True, move_time=1))
    await myvts.close()

async def zoomin(myvts: pyvts.vts):
    await myvts.connect()
    await myvts.request_authenticate()
    await myvts.request(
        myvts.vts_request.requestMoveModel(0,0,size=10, relative=True, move_time=1))
    await myvts.close()

async def getItems(myvts: pyvts.vts):
    await myvts.connect()
    await myvts.request_authenticate()
    response = await myvts.request(
        myvts.vts_request.requestItemList(False, True, False))
    print(response)
    await myvts.close()

async def toggleHeadpat(myvts: pyvts.vts, seconds: int):
    await myvts.connect()
    await myvts.request_authenticate()
    response = await myvts.request(
        myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=1))
    time.sleep(seconds)
    response = await myvts.request(
        myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=0))
    await myvts.close()

async def turboHeadpat(myvts: pyvts.vts, seconds: int):
    await myvts.connect()
    await myvts.request_authenticate()
    response = await myvts.request(
        myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=1, framerate=60))
    time.sleep(seconds)
    response = await myvts.request(
        myvts.vts_request.requestItemAnimationControl('b5a7e8ba1c0b42eda2460328618da2cb', opacity=0))
    await myvts.close()

async def zoomMoustache(myvts: pyvts.vts):
    print("hello")
    await myvts.connect()
    await myvts.request_authenticate()
    response = await myvts.request(
        myvts.vts_request.requestItemMove('93dd087fedcd44dda640fa72e13c6bd5',positionX=0.1,rotation=90, size=0.5))
    print(response)
    await myvts.close()