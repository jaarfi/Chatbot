import jaarfivts
import models
import asyncio
import time
import nest_asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import asyncio
from dataclasses import dataclass
from typing import Callable, Optional, ClassVar

from async_tkinter_loop import async_handler, async_mainloop

nest_asyncio.apply()


@dataclass
class WorkItem:
    request: models.BaseRequest
    response: models.BaseResponse
    callback_function: Optional[Callable]

async def worker(name, request_queue: asyncio.Queue, response_queue: asyncio.Queue, vts: jaarfivts.JaarfiVts):
    await vts.connect()
    await vts.authenticate(models.AuthenticationTokenRequest())

    # Get a "work item" out of the queue.
    while request_queue.qsize() != 0:
        work_item = await request_queue.get()
        response= await vts.request(work_item.request)
        if work_item.callback_function:
            response = work_item.response.model_validate(response)
            work_item.callback_function(response)

        print(f'{name} has requested {work_item.request.message_type} and there are {request_queue.qsize()} items left')

    await vts.close()

async def flip(request_queue: asyncio.Queue):
    for i in range(120):
        await request_queue.put(
            WorkItem(
                request= models.MoveModelRequest(
                    data=models.MoveModelRequestData(
                        time_in_seconds=0,
                        values_are_relative_to_model=True,
                        rotation=6,
                        size=0,
                    )
                ),
                response=models.ColorTintResponse,
                callback_function=None
            )
        )
        await asyncio.sleep(1/60)

async def rainbow(request_queue: asyncio.Queue):
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
                await request_queue.put(
                    WorkItem(
                        request= models.ColorTintRequest(
                            data = models.ColorTintRequestData(
                                color_tint=models.ColorTint(
                                color_r=colors[1],
                                color_b=colors[2],
                                color_g=colors[0] 
                                ),
                                art_mesh_matcher=models.ArtMeshMatcher(
                                    tint_all=True
                                )
                            )
                        ),
                        response=models.ColorTintResponse,
                        callback_function=None
                    )
                )
                await asyncio.sleep(1/60)
            increase = not increase
    return



async def getCurrentModelSize(request_queue: asyncio.Queue):
    await request_queue.put(
        WorkItem(
            request=models.CurrentModelRequest(),
            response=models.CurrentModelResponse,
            callback_function=lambda response: popUp(response.data.model_position.size)
            )
    )
    

async def metaWorker(meta_queue: asyncio.Queue):
    while True:
        request = await meta_queue.get()
        
        request_queue = asyncio.Queue()
        response_queue = asyncio.Queue()
        asyncio.create_task(worker(f'worker', request_queue, response_queue, jaarfivts.JaarfiVts(ws_ip="127.0.0.1")))
        print("got em")
        asyncio.create_task(request(request_queue))

def popUp(message):
    messagebox.showinfo(message)

async def guitask(meta_queue):
    root = tk.Tk() 

    root.geometry("500x500")
    a = ttk.Label(root, text ="Hello World")
    ttk.Button(root, text="flip", command=lambda: asyncio.run(meta_queue.put(flip))).pack()
    ttk.Button(root, text="rainbow", command=lambda: asyncio.run(meta_queue.put(rainbow))).pack()
    ttk.Button(root, text="sitze", command=lambda: asyncio.run(meta_queue.put(getCurrentModelSize))).pack()

    a.pack()

    async_mainloop(root)

async def printafter():
    await asyncio.sleep(1)
    print("after")

async def main():
    asyncio.create_task(metaWorker(meta_queue))
    asyncio.create_task(guitask(meta_queue))
    await asyncio.sleep(0)
    #asyncio.create_task(fun.flip(request_queue))
    #size = await fun.getCurrentModelSize(request_queue, response_queue)
    #print(size)
    #asyncio.create_task(fun.rainbow(request_queue))

meta_queue = asyncio.Queue()

asyncio.run(main())

