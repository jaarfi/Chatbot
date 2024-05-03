import tkinter as Tk
import asyncio
import threading
import consumercoro
import vtsFunctions
from events import Events
from testbot import Bot
import Jaarfivts.models as models
from tkinter import ttk

loop = asyncio.get_event_loop()
threading.Thread(daemon=True, target=loop.run_forever).start()
trigger_dict = {}
bot = Bot(trigger_dict)
fun_dict = {}


def on_start():
    print("start")
    asyncio.run_coroutine_threadsafe(bot.connect(), loop)


def on_flip():
    print("flip")
    asyncio.run_coroutine_threadsafe(consumercoro.manager(consumercoro.big), loop)


def on_stop():
    print("stop")
    asyncio.run_coroutine_threadsafe(bot.stop(), loop)


def sparkle(_):
    print("****")
    asyncio.run_coroutine_threadsafe(
        consumercoro.manager(
            [
                [lambda: vtsFunctions.activateExpression("expression2.exp3.json")],
                [lambda: vtsFunctions.putCoroIntoDeque(asyncio.sleep(1))],
                [lambda: vtsFunctions.deactivateExpression("expression2.exp3.json")],
            ]
        ),
        loop,
    )


def meow(_):
    print("****")
    asyncio.run_coroutine_threadsafe(
        consumercoro.manager(
            [
                [lambda: vtsFunctions.activateExpression("meow.exp3.json")],
                [lambda: vtsFunctions.putCoroIntoDeque(asyncio.sleep(1))],
                [lambda: vtsFunctions.deactivateExpression("meow.exp3.json")],
            ]
        ),
        loop,
    )


def manager(funlist):
    asyncio.run_coroutine_threadsafe(
        consumercoro.manager(funlist),
        loop,
    )


def addtrigger(trigger, function):
    print(trigger, function)
    global trigger_dict
    if trigger in trigger_dict.keys():
        trigger_dict[trigger].on_change += function
        return
    event = Events()
    event.on_change += function
    trigger_dict[trigger] = event


class GUI:
    def __init__(self) -> None:
        self.expressions = None
        self.connections = []
        self.root = Tk.Tk()
        self.clicked = Tk.StringVar()
        self.options = ["a", "b"]
        self.optionMenu = ttk.OptionMenu(self.root, self.clicked, *self.options)
        on_start()
        manager([[lambda: vtsFunctions.saveExpressions(self.setExpressions)]])
        self.guitask()

    def setExpressions(self, expressionResponse: models.ExpressionStateResponse):
        global fun_dict
        self.expressions = expressionResponse.data.expressions
        self.optionMenu["menu"].delete(0, "end")
        if self.expressions:
            self.clicked.set(self.expressions[0].name)
            for exp in self.expressions:
                fun_dict[exp.name] = exp.file
                self.optionMenu["menu"].add_command(
                    label=exp.name, command=Tk._setit(self.clicked, exp.name)
                )

    def guitask(self):
        frame = Tk.Frame(self.root)

        E1 = ttk.Entry(self.root)
        E1.pack(side="left")
        stop_button = ttk.Button(
            frame.master,
            text="add",
            command=lambda: addtrigger(
                E1.get(),
                lambda _, name = self.clicked.get(): manager(
                    [
                        [lambda: vtsFunctions.activateExpression(fun_dict[name])],
                        [lambda: vtsFunctions.putCoroIntoDeque(asyncio.sleep(1))],
                        [lambda: vtsFunctions.deactivateExpression(fun_dict[name])],
                    ]
                ),
            ),
        )
        stop_button.pack(side="right")
        self.optionMenu.pack()

        self.root.mainloop()


if __name__ == "__main__":
    GUI()
