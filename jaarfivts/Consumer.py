import jaarfivts
import asyncio
from typing import Coroutine, Optional, List
import models
from random import choice
from string import ascii_uppercase
from faker import Faker


class Consumer:
    def __init__(
        self, providers_formatted: List[List[Coroutine]], queue: asyncio.Queue
    ) -> None:
        # create a new VTS connection for each Worker
        self.queue = queue

        asyncio.create_task(self.manager(providers_formatted))

    async def manager(self, providers_formatted: List[List[Coroutine]]):
        for simultaneous in providers_formatted:
            event_list = []
            counter = 0
            for provider in simultaneous:
                asyncio.create_task(provider)
                counter -= -1
            for i in range(counter):
                event = asyncio.Event()
                event_list.append(event)
                asyncio.create_task(self.consumer(event))
            for event in event_list:
                await event.wait()
        print("feddich")

    async def consumer(self, event):
        """
        works of work_items in the queue
        """
        vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
        await vts.connect()
        await vts.authenticate(models.AuthenticationTokenRequest())

        fake = Faker()
        name = fake.name()
        # Get a "work item" out of the queue.
        while True:
            while self.queue.qsize() != 0:
                # while theres stuff in the queue it gets the first one
                work_item = await self.queue.get()

                # because workitems can contain requests OR coros, we have to differentiate
                work = work_item.work_to_be_done
                if isinstance(work, models.BaseRequest):
                    # sends the request to vts
                    response = await vts.request(work)
                else:
                    # if its not a request, then its a coro to be awaited
                    await work

                # if we want a callback, it is called
                if work_item.callback_function:
                    response = work_item.response.model_validate(response)
                    work_item.callback_function(response)

                self.queue.task_done()
                print(
                    f"{name} requested / worked on {work} and there are {self.queue.qsize()} items left"
                )
            await asyncio.sleep(1 / 60)

            # just check again if the q is empty, maybe another thread is writing slower than were using
            if self.queue.qsize() == 0:
                print(
                    f"{name} saw their queue was empty, so they walked into the water with stones in their pockets"
                )
                event.set()
                break

        # close the connection at the end, it would timeout anyway
        await vts.close()
