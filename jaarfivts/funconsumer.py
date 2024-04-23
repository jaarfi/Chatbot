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
from typing import Callable, Optional, ClassVar, List, Union, Coroutine
import Worker
import faker
import Consumer

from async_tkinter_loop import async_handler, async_mainloop

nest_asyncio.apply()
expressions = List[models.SingleExpression]

root = tk.Tk()
request_queue = asyncio.Queue()


@dataclass
class WorkItem:
    work_to_be_done: Union[models.BaseRequest, Coroutine]
    response: models.BaseResponse
    callback_function: Optional[Callable] = None
    event: asyncio.Event = None


async def create_gui():
    gui = GUI()
    await gui._ainit()


class DragDropListbox(tk.Listbox):
    """A Tkinter listbox with drag'n'drop reordering of entries."""

    def __init__(self, master, **kw):
        kw["selectmode"] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind("<Button-1>", self.setCurrent)
        self.bind("<B1-Motion>", self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


class GUI:
    def __init__(self) -> None:
        self.expressions = None
        self.v = tk.IntVar()
        self.v.set(1)
        self.trigger_response_connections = []
        self.actions_dict = {}
        self.q = asyncio.Queue()
        pass

    async def _ainit(self):
        asyncio.create_task(self.guitask())
        await asyncio.sleep(0)

    def flipCaller(self, rotations: int):
        return self.flip(rotations, self.q)
    
    async def flip(self, rotations: int, request_queue: asyncio.Queue):
        for i in range(60 * rotations):
            await request_queue.put(
                WorkItem(
                    work_to_be_done=models.MoveModelRequest(
                        data=models.MoveModelRequestData(
                            time_in_seconds=0,
                            values_are_relative_to_model=True,
                            rotation=6,
                            size=0,
                        )
                    ),
                    response=models.ColorTintResponse,
                )
            )
            await asyncio.sleep(1 / 60)

    def rainbowCaller(self):
        return self.rainbow(self.q)

    async def rainbow(self, request_queue: asyncio.Queue):
        print("im in rainbow")
        increase = True
        colors = [0, 255, 0]
        change = 20
        for i in range(2):
            for color in range(3):
                for i in range(int(255 / change)):
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
                            work_to_be_done=models.ColorTintRequest(
                                data=models.ColorTintRequestData(
                                    color_tint=models.ColorTint(
                                        color_r=colors[1],
                                        color_b=colors[2],
                                        color_g=colors[0],
                                    ),
                                    art_mesh_matcher=models.ArtMeshMatcher(
                                        tint_all=True
                                    ),
                                )
                            ),
                            response=models.ColorTintResponse,
                        )
                    )
                    await asyncio.sleep(1 / 60)
                increase = not increase

    def getCurrentModelSizeCaller(self):
        return self.getCurrentModelSize(self, self.q)
    
    async def getCurrentModelSize(self, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                work_to_be_done=models.CurrentModelRequest(),
                response=models.CurrentModelResponse,
                callback_function=lambda response: self.popUp(
                    response.data.model_position.size
                ),
            )
        )

    def saveExpressionsCaller(self):
        return self.saveExpressions(self.q)

    async def saveExpressions(self, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                work_to_be_done=models.ExpressionStateRequest(),
                response=models.ExpressionStateResponse,
                callback_function=lambda response: self.setExpressions(
                    response.data.expressions
                ),
            )
        )

    def setExpressions(self, expressions):
        self.expressions = expressions

    def toggleExpressionCaller(self, file):
        return self.toggleExpression(file, self.q)

    async def toggleExpression(self, file: str, request_queue: asyncio.Queue):
        expression_currently_active = [
            exp.active for exp in self.expressions if exp.file == file
        ]
        expression_currently_active = expression_currently_active[0]
        await request_queue.put(
            WorkItem(
                work_to_be_done=models.ExpressionActivationRequest(
                    data=models.ExpressionActivationRequestData(
                        expression_file=file, active=not expression_currently_active
                    )
                ),
                response=models.ExpressionActivationResponse,
            )
        )

    async def coroQueuePutterCaller(self, coro):
        return self.coroQueuePutter(coro, self.q)

    async def coroQueuePutter(self, coro, queue):
        await queue.put(WorkItem(work_to_be_done=coro, response=models.BaseResponse))

    async def guitask(self):
        root.geometry("500x500")

        q = asyncio.Queue()
        a = [self.flipCaller(1), self.rainbowCaller()]
        b = [self.saveExpressionsCaller()]
        c = [
            self.toggleExpressionCaller("expression2.exp3.json"),
            self.toggleExpressionCaller("meow.exp3.json"),
        ]
        d = [self.coroQueuePutterCaller(asyncio.sleep(1))]
        e = [self.saveExpressionsCaller(q)]
        f = [
            self.toggleExpressionCaller("expression2.exp3.json"),
            self.toggleExpressionCaller("meow.exp3.json"),
        ]
        big = [b, c, d, e, f]
        ttk.Button(
            root,
            text="not wait",
            command=lambda: Consumer.Consumer(self.callerToCoro(big), self.q),
        ).pack()

        async_mainloop(root)

    def callerToCoro(self, list):
        self.q = asyncio.Queue()
        newlist = []
        for x in list:
            sublist = []
            for y in x:
                sublist.append(y())
            newlist.append(sublist)
        return newlist


if __name__ == "__main__":
    asyncio.run(create_gui())
