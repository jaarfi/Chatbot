# import VTSconn.models as models
from Jaarfivts import models
from Jaarfivts import jaarfivts
import asyncio
import nest_asyncio
import tkinter as tk
from tkinter import ttk
import asyncio
import consumer
import vtsFunctions
from events import Events
import random
from async_tkinter_loop import async_mainloop
from dataclasses import dataclass
from typing import List, Callable
import threading
import twitch

nest_asyncio.apply()


@dataclass
class triggerAction:
    trigger: str
    actions: List[List[Callable]]


class GUI:
    def __init__(self) -> None:
        self.expressions = None
        self.connections = []
        self.guitask()

    def setExpressions(self, expressionResponse: models.ExpressionStateResponse):
        self.expressions = expressionResponse.data.expressions

    def guitask(self):
        root = tk.Tk()
        root.geometry("500x500")
        print("hoola")

        a = [lambda: vtsFunctions.flip(1, 1), lambda: vtsFunctions.rainbow()]
        b = [lambda: vtsFunctions.saveExpressions(self.setExpressions)]
        c = [lambda: vtsFunctions.toggleExpression(self.expressions, "meow.exp3.json")]
        d = [lambda: vtsFunctions.putCoroIntoDeque(asyncio.sleep(1))]
        e = [lambda: vtsFunctions.saveExpressions(self.setExpressions)]
        f = [lambda: vtsFunctions.toggleExpression(self.expressions, "meow.exp3.json")]
        big = [a, b, c, d, e, f]

        event_list = []
        for i in range(5):
            event = Events()
            event_list.append(event)
            ttk.Button(
                root,
                text="Button" + str(i),
                command=lambda: consumer.Consumer(big),
            ).pack(fill="x", side="bottom")
            event.on_change += self.printEvent

        ttk.Button(
            root, text="Bind", command=lambda: self.helper(event_list, big)
        ).pack(fill="x", side="bottom")

        async_mainloop(root)
        loop = asyncio.get_event_loop()
        threading.Thread(daemon=True, target=loop.run_forever).start()
        asyncio.run_coroutine_threadsafe(loop, twitch.start())

    def printEvent(self, i):
        print("This was triggered by button", i)

    def helper(self, event_list, big):
        random.choice(event_list).on_change += lambda i: consumer.Consumer(big)


def startGui():
    gui = GUI()


if __name__ == "__main__":
    startGui()
