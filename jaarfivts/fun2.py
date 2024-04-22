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
import faker

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
        pass

    def popUp(self, message):
        messagebox.showinfo(message)

    async def guitask(self):
        q = asyncio.Queue()
        e = asyncio.Event()
        Worker.Worker(self.saveExpressions(e, q), q)
        asyncio.run(e.wait())

        root.geometry("500x500")
        labelframe = ttk.LabelFrame(root, text="Trigger-Action Connections")

        m = tk.Menu(root, tearoff=0)
        m.add_command(
            label="Add new Connection",
            command=lambda: self.popup_trigger_action(labelframe),
        )

        ttk.Button(root, text="flip", command=self.fliphelper).pack()

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        labelframe.bind("<Button-3>", do_popup)

        labelframe.pack(fill="both", expand=True, side="bottom")

        async_mainloop(root)

    def popup_trigger_action(self, root):
        win = tk.Toplevel()
        win.wm_title("Window")
        win.geometry("500x500")

        triggers = ttk.LabelFrame(win, text="Triggers")
        actions = ttk.LabelFrame(win, text="Actions")
        listbox = DragDropListbox(actions)

        actions_menu = tk.Menu(win, tearoff=0)

        expression_add_menu = tk.Menu(root, tearoff=0)

        counter = 0

        def helper(expression):
            print(expression.name)
            listbox.insert(1, expression.name)

        for expression in self.expressions:
            self.actions_dict[expression.name] = (
                lambda expression=expression: self.togglehelper(expression)
            )
            expression_add_menu.add_command(
                label=expression.name,
                command=lambda expression=expression: helper(expression),
            )

        actions_menu.add_cascade(label="Expressions", menu=expression_add_menu)

        def do_popup_actions(event):
            try:
                actions_menu.tk_popup(event.x_root, event.y_root)
            finally:
                actions_menu.grab_release()

        listbox.pack()
        actions.bind("<Button-3>", do_popup_actions)
        actions.pack(fill="both", expand=True, side="right")
        triggers.pack(fill="both", expand=True, side="left")

        def helper2():
            listbox_list = listbox.get(0, "end")
            command_list = [self.actions_dict[item] for item in listbox_list]
            for command in command_list:
                command()
            win.destroy()

        ttk.Button(win, text="Okay", command=helper2).pack(side="bottom")

    def popup_trigger_response(self, root):
        win = tk.Toplevel()
        win.wm_title("Window")

        self.v.set(0)

        for i, expression in enumerate(self.expressions):
            ttk.Radiobutton(
                win,
                text=expression.name,
                variable=self.v,
                command=lambda: print("b"),
                value=i,
            ).grid()

        def helper():
            self.newExpressionItem(root, self.expressions[self.v.get()])
            win.destroy()

        ttk.Button(win, text="Okay", command=helper).grid()

    def togglehelper(self, expression):
        q = asyncio.Queue()
        event = asyncio.Event()
        kill_event = asyncio.Event()
        Worker.Worker(
            self.toggleExpression(expression.file, kill_event, q), q, kill_event
        )

    def fliphelper(self):
        q = asyncio.Queue()
        Worker.Worker(self.flip(q, 1), q)

    def newExpressionItem(self, root, expression):
        l = ttk.Label(root, text=expression.name)
        m = tk.Menu(root, tearoff=0)
        m.add_command(label="Delete", command=l.destroy)

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        l.bind("<Button-3>", do_popup)
        l.pack()


if __name__ == "__main__":
    asyncio.run(create_gui())
