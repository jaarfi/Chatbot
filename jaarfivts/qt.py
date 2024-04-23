import asyncio
from faker import Faker

fake = Faker()

async def person(name):
    while True:
        print(name, "wants to tell you that they loves you")
        await asyncio.sleep(0.5)

async def main():
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(4):
        name = fake.name()
        tasks.append(loop.create_task(person(name)))
        await asyncio.sleep(0.2)
    loop.run_until_complete(tasks)
    

asyncio.run(main())