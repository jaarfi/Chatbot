import Jaarfivts.jaarfivts as jaarfivts
import asyncio
from typing import List, Callable
import Jaarfivts.models as models
from faker import Faker
from collections import deque
from dataclasses import dataclass
import vtsFunctions


a = [lambda: vtsFunctions.flip(1, 1), lambda: vtsFunctions.rainbow()]
c = [lambda: vtsFunctions.activateExpression("meow.exp3.json")]
d = [lambda: vtsFunctions.putCoroIntoDeque(asyncio.sleep(1))]
f = [lambda: vtsFunctions.deactivateExpression("meow.exp3.json")]
big = [a, c, d, f]


@dataclass
class consumerConfig:
    deq: deque
    event: asyncio.Event
    vts: jaarfivts.JaarfiVts


def __init__(self, providers_formatted: List[List[Callable]]) -> None:
    try:
        asyncio.create_task(self.manager(providers_formatted))
    except RuntimeError as e:
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.manager(providers_formatted))
        loop.run_until_complete(task)


async def manager(providers_formatted: List[List[Callable]]):
    print("get micromanaged, idiot")
    for simultaneous in providers_formatted:
        done_events = []
        start_event = asyncio.Event()

        for provider in simultaneous:
            deq = provider()
            done_event = asyncio.Event()
            done_events.append(done_event)

            vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
            await vts.connect()
            await vts.authenticate(models.AuthenticationTokenRequest())

            asyncio.create_task(consumer(deq, done_event, vts, start_event))
        start_event.set()
        for event in done_events:
            await event.wait()


async def consumer(deq: deque, done_event, vts, start_event):
    """
    works of work_items in the queue
    """

    fake = Faker()
    name = fake.name()
    await start_event.wait()
    while deq:
        work_item = deq.popleft()
        work = work_item.work_to_be_done

        if isinstance(work, models.BaseRequest):
            
            print(f"{name} starter request for {work.message_type}")
            response = await vts.request(work)
            response = work_item.response.model_validate_json(response)
            if response.message_type == "APIError":
                pass
                print(
                    f"{name} requested {work.message_type} and got error response {response.data.message}"
                )
            else:
                print(f"{name} succesfully requested {work.message_type}")

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
    done_event.set()

    # close the connection at the end, it would timeout anyway
    await vts.close()
