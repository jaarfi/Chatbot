import jaarfivts
import models
import asyncio
import time
import nest_asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import fun2
import time
import asyncio
  
nest_asyncio.apply()


async def create_fun(settings):
    fun = Fun(settings)
    await fun._init()
    return fun



async def worker(name, request_queue: asyncio.Queue, response_queue: asyncio.Queue, vts: jaarfivts.JaarfiVts):
    while True:
        # Get a "work item" out of the queue.
        request = await request_queue.get()
        if isinstance(request, list):
            event = request[1]
            request = request[0]
            result = await vts.request(request)
            await response_queue.put(result)
            event.set()
        else:
            await vts.request(request)
        request_queue.task_done()

        print(f'{name} has requested {request.message_type} and there are {request_queue.qsize()} items left')


class Fun:
    def __init__(self, vts: jaarfivts.JaarfiVts) -> None:
        self.vts = vts
        pass

    async def _init(self):
        await self.vts.connect()
        await self.vts.authenticate(models.AuthenticationTokenRequest())

    async def flip(self, request_queue: asyncio.Queue):
        print("im in fli")
        for i in range(120):
            await request_queue.put(
                models.MoveModelRequest(
                    data=models.MoveModelRequestData(
                        time_in_seconds=0,
                        values_are_relative_to_model=True,
                        rotation=6,
                        size=0,
                    )
                )
            )
            await asyncio.sleep(1/60)

    async def rainbow(self,  request_queue: asyncio.Queue):
        print("im in rainbow")
        increase = True
        colors = [0, 255, 0]
        change = 20
        for i in range(2):
            for color in range(3):
                for i in range(int(255/change)):
                    if increase:
                        colors[color] = colors[color] + change
                        if colors[color] > 255:
                            colors[color] = 255
                    else:
                        colors[color] = colors[color] - change
                        if colors[color] < 0:
                            colors[color] = 0
                    await request_queue.put(models.ColorTintRequest(
                        data=models.ColorTintRequestData(
                            color_tint=models.ColorTint(
                            color_r=colors[1],
                            color_b=colors[2],
                            color_g=colors[0] 
                            ),
                            art_mesh_matcher=models.ArtMeshMatcher(
                                tint_all=True
                            )
                        )
                    ))
                    await asyncio.sleep(1/60)
                increase = not increase

    async def getCurrentModelSize(self,  request_queue: asyncio.Queue,  response_queue: asyncio.Queue):
        event = asyncio.Event()
        response = await request_queue.put([models.CurrentModelRequest(),event])
        await event.wait()
        response = await response_queue.get()
        response_queue.task_done()
        response = models.CurrentModelResponse.model_validate(response)
        return response.data.model_position.size
    

async def metaWorker(meta_queue: asyncio.Queue):
    while True:
        request = await meta_queue.get()
        asyncio.create_task(request)



async def main():
    asyncio.create_task(worker(f'worker', request_queue, response_queue, settings))
    asyncio.create_task(fun.flip(request_queue))
    size = await fun.getCurrentModelSize(request_queue, response_queue)
    print(size)
    asyncio.create_task(fun.rainbow(request_queue))
    await asyncio.sleep(10)

settings = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
fun = asyncio.run(create_fun(settings))

request_queue = asyncio.Queue()
response_queue = asyncio.Queue()
meta_queue = asyncio.Queue()

asyncio.run(main())

