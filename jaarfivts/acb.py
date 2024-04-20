import asyncio
import random
import time
import fun


async def worker(name, queue: asyncio.Queue):
    while True:
        # Get a "work item" out of the queue.
        request = await queue.get()
        await asyncio.sleep(1/60)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has requested {request}')


async def boss(name, queue: asyncio.Queue):
    number_frames = random.choice(range(50, 100))
    print(number_frames)
    for i in range(number_frames):
        frame = f'{name} frame number {i}'
        await queue.put(frame)
        await asyncio.sleep(0.001)

        #print(f'{name} has put in a {frame} into the queue')



async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(1):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)
    for i in range(10):
        task = asyncio.create_task(boss(f'boss-{i}', queue))
        tasks.append(task)

    await asyncio.sleep(100)
    # Wait until the queue is fully processed.
    started_at = time.monotonic()


asyncio.run(main())