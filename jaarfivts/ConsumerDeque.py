import jaarfivts
import asyncio
from typing import List, Callable
import models
from faker import Faker
from collections import deque
from time import process_time


class Consumer:
    def __init__(
        self, 
        providers_formatted: List[List[Callable]]
    ) -> None:
        asyncio.create_task(self.manager(providers_formatted))

    async def manager(self, providers_formatted: List[List[Callable]]):
        for simultaneous in providers_formatted:
            event_list = []
            for provider in simultaneous:
                event = asyncio.Event()
                event_list.append(event)
                vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
                await vts.connect()
                await vts.authenticate(models.AuthenticationTokenRequest())
                asyncio.create_task(self.consumer(event, provider(), vts))
            await asyncio.sleep(0)
            for event in event_list:
                await event.wait()

    async def consumer(self, event, deq: deque, vts):
        """
        works of work_items in the queue
        """
        

        fake = Faker()
        name = fake.name()
        print(f"{name} has started working")
        
        dummy = await vts.request(models.APIStateRequest())
        while deq:
            work_item = deq.popleft()

            work = work_item.work_to_be_done
            if isinstance(work, models.BaseRequest):
                t = process_time()
                response = await vts.request(work)
                diff = process_time() - t
                response = work_item.response.model_validate_json(response)
                if response.message_type == "APIError":
                    pass
                    print(
                        f"{name} requested {work.message_type} and got error response {response.data.message}"
                    )
                else:
                    pass
                    print(
                        f"{name} succesfully requested {work.message_type} and it took {diff} seconds"
                    )

            else:
                print(
                        f"{name} will await {work} after this short message from out sponsors: NIKE"
                    )
                await work

            if work_item.callback_function:
                work_item.callback_function(response)
        print(
            f"{name} saw their queue was empty, so they walked into the water with stones in their pockets"
        )
        event.set()

        # close the connection at the end, it would timeout anyway
        await vts.close()
