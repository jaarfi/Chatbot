import jaarfivts
import asyncio
from typing import Coroutine, Optional
import models
from random import choice
from string import ascii_uppercase
from faker import Faker


class Worker:
    def __init__(
        self,
        coroutine: Coroutine,
        queue: asyncio.Queue,
        kill_event: Optional[asyncio.Event] = None,
    ) -> None:
        # create a new VTS connection for each Worker
        self.vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
        self.queue = queue
        if kill_event == None:
            kill_event = asyncio.Event()
            kill_event.set()
        self.kill_event = kill_event
        asyncio.create_task(self.worker())
        asyncio.create_task(coroutine)

    async def worker(self):
        """
        works of work_items in the queue
        """
        await self.vts.connect()
        await self.vts.authenticate(models.AuthenticationTokenRequest())

        fake = Faker()
        name = fake.name()
        # Get a "work item" out of the queue.
        while True:
            while self.queue.qsize() != 0:
                # while theres stuff in the queue it gets the first one
                work_item = await self.queue.get()
                # sends the request to vts
                response = await self.vts.request(work_item.request)
                # if we want a callback, it is called
                if work_item.callback_function:
                    response = work_item.response.model_validate(response)
                    work_item.callback_function(response)

                if work_item.event:
                    work_item.event.set()

                print(
                    f"{name} requested {work_item.request.message_type} and there are {self.queue.qsize()} items left"
                )
            if self.kill_event._value:
                print(f"{name} committed sudoku")
                break
            await asyncio.sleep(1 / 60)
            print(f"{name} is going for another round")

        # close the connection at the end, it would timeout anyway
        await self.vts.close()
