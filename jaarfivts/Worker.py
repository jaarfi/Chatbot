import jaarfivts
import asyncio
from typing import Callable
import models

async def create_worker(function: Callable):
    worker = Worker(function)
    await worker._ainit()


class Worker:
    def __init__(self, function: Callable) -> None:
        self.vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
        self.queue = asyncio.Queue()
        self.function = function
        pass

    async def _ainit(self):
        asyncio.create_task(self.worker())
        asyncio.create_task(self.function(self.queue))
    
    async def worker(self):
        await self.vts.connect()
        await self.vts.authenticate(models.AuthenticationTokenRequest())

        # Get a "work item" out of the queue.
        while self.queue.qsize() != 0:
            work_item = await self.queue.get()
            response= await self.vts.request(work_item.request)
            if work_item.callback_function:
                response = work_item.response.model_validate(response)
                work_item.callback_function(response)

            print(f'requested {work_item.request.message_type} and there are {self.queue.qsize()} items left')

        await self.vts.close()