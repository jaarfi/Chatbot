import events
from events import Events
import asyncio

def foo(reason):
    print("foo",reason)

def bar(reason):
    print("bar",reason)

def baz(reason):
    print("baz",reason)



events = Events()
events.on_change += foo
events.on_change += baz
events.on_change += bar

events.on_change("manually triggered")

async def asyncTrigger():
    while True:
        events.on_change("async trigger")
        await asyncio.sleep(0.5)

asyncio.run(asyncTrigger())