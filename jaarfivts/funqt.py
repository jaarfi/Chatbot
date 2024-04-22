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
from typing import Callable, Optional, ClassVar, List
import Worker

from async_tkinter_loop import async_handler, async_mainloop

nest_asyncio.apply()
expressions = List[models.SingleExpression]

root = tk.Tk()
request_queue = asyncio.Queue()


@dataclass
class WorkItem:
    request: models.BaseRequest
    response: models.BaseResponse
    callback_function: Optional[Callable] = None
    event: asyncio.Event = None


async def create_gui():
    gui = GUI()
    await gui._ainit()


class GUI:

    def __init__(self) -> None:
        self.expressions = None
        self.v = tk.IntVar()
        self.v.set(1)
        pass

    async def _ainit(self):
        asyncio.create_task(self.guitask())
        await asyncio.sleep(0)

    async def flip(self, request_queue: asyncio.Queue, rotation: int):
        for i in range(60 * rotation):
            await request_queue.put(
                WorkItem(
                    request=models.MoveModelRequest(
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
                            request=models.ColorTintRequest(
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

    async def getCurrentModelSize(self, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                request=models.CurrentModelRequest(),
                response=models.CurrentModelResponse,
                callback_function=lambda response: self.popUp(
                    response.data.model_position.size
                ),
            )
        )

    async def saveExpressions(self, event, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                request=models.ExpressionStateRequest(),
                response=models.ExpressionStateResponse,
                callback_function=lambda response: self.setExpressions(
                    response.data.expressions
                ),
                event=event,
            )
        )

    def setExpressions(self, expressions):
        self.expressions = expressions

    async def activateExpression(self, file: str, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                request=models.ExpressionActivationRequest(
                    data=models.ExpressionActivationRequestData(
                        expression_file=file, active=True
                    )
                ),
                response=models.ExpressionActivationResponse,
            )
        )

    async def deactivateExpression(self, file: str, request_queue: asyncio.Queue):
        await request_queue.put(
            WorkItem(
                request=models.ExpressionActivationRequest(
                    data=models.ExpressionActivationRequestData(
                        expression_file=file, active=False
                    )
                ),
                response=models.ExpressionActivationResponse,
            )
        )

    async def toggleExpression(
        self, file: str, kill_event, request_queue: asyncio.Queue
    ):
        event = asyncio.Event()

        await self.saveExpressions(event, request_queue)
        await event.wait()

        expression_currently_active = [
            exp.active for exp in self.expressions if exp.file == file
        ]
        expression_currently_active = expression_currently_active[0]
        await request_queue.put(
            WorkItem(
                request=models.ExpressionActivationRequest(
                    data=models.ExpressionActivationRequestData(
                        expression_file=file, active=not expression_currently_active
                    )
                ),
                response=models.ExpressionActivationResponse,
            )
        )
        kill_event.set()

    def popUp(self, message):
        messagebox.showinfo(message)

    async def guitask(self):
        q = asyncio.Queue()
        Worker.Worker(self.saveExpressions(asyncio.Event(), q), q)

        root.geometry("500x500")
        a = ttk.Label(root, text="Hello World")
        ttk.Button(
            root,
            text="flip",
            command=lambda q=asyncio.Queue(): Worker.Worker(self.flip(q, 1), q),
        ).pack()
        ttk.Button(
            root,
            text="rainbow",
            command=lambda q=asyncio.Queue(): Worker.Worker(self.rainbow(q), q),
        ).pack()
        ttk.Button(
            root,
            text="exp",
            command=lambda q=asyncio.Queue(): Worker.Worker(self.saveExpressions(q), q),
        ).pack()
        ttk.Button(
            root,
            text="size",
            command=lambda q=asyncio.Queue(): Worker.Worker(
                self.getCurrentModelSize(q), q
            ),
        ).pack()
        ttk.Button(
            root,
            text="prit",
            command=lambda: print(self.expressions),
        ).pack()
        ttk.Button(root, text="Bonuses", command=self.popup_bonus).pack()
        ttk.Button(root, text="readio", command=self.popup_trigger_response).pack()
        ttk.Button(
            root,
            text="toggle",
            command=lambda: self.helper(self.expressions[self.v.get()]),
        ).pack()

        a.pack()

        async_mainloop(root)

    def popup_bonus(self):
        win = tk.Toplevel()
        win.wm_title("Window")

        l = tk.Label(win, text="Input")
        l.grid(row=0, column=0)

        for i, expression in enumerate(self.expressions):
            ttk.Button(
                win,
                text=expression.name,
                command=lambda expression=expression: self.helper(expression),
            ).grid(row=i, column=0)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=1, column=0)

    def popup_trigger_response(self):
        win = tk.Toplevel()
        win.wm_title("Window")

        l = tk.Label(win, text="Input")
        b = ttk.Button(win, text="Okay", command=win.destroy).pack()
        self.v.set(0)

        for i, expression in enumerate(self.expressions):
            ttk.Radiobutton(
                root, text=expression.name, variable=self.v, command=print(), value=i
            ).pack()

    def helper(self, expression):
        q = asyncio.Queue()
        kill_event = asyncio.Event()
        Worker.Worker(
            self.toggleExpression(expression.file, kill_event, q), q, kill_event
        )

    def helper2(self):
        q = asyncio.Queue()
        kill_event = asyncio.Event()
        expression = self.expressions[self.v.get()]
        Worker.Worker(
            self.toggleExpression(expression.file, kill_event, q), q, kill_event
        )


if __name__ == "__main__":
    asyncio.run(create_gui())
