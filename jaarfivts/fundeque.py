import models
import asyncio
import nest_asyncio
import tkinter as tk
from tkinter import ttk
import asyncio
import ConsumerDeque
import higher
from events import Events
import random
from async_tkinter_loop import async_mainloop
import jaarfivts

nest_asyncio.apply()

class GUI:
    def __init__(self) -> None:
        self.expressions = None
        self.guitask()
        #asyncio.run(self.guitask())

    def setExpressions(self, expressionResponse: models.ExpressionStateResponse):
        self.expressions = expressionResponse.data.expressions

    def guitask(self):
        root = tk.Tk()
        root.geometry("500x500")

        async def initConnect():
            vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
            await vts.connect()
            await vts.authenticate(models.AuthenticationTokenRequest())
            response = await vts.request(models.APIStateRequest())
            response = models.APIStateResponse.model_validate_json(response)
            if response.message_type == "APIError":
                print("We got an APIError when trying to connect to it with the message",response.data.message, "please fix and try again")
                return
            print(response.data.model_dump_json())
                            
        asyncio.run(initConnect())

        a = [lambda: higher.flip(0.5,1),lambda: higher.flip(0.5,1)]
        b = [lambda: higher.saveExpressions(lambda exp:self.setExpressions(exp))]
        c = [lambda: higher.toggleExpression(self.expressions, "meow.exp3.json")]
        d = [lambda: higher.putCoroIntoDeque(asyncio.sleep(1))]
        e = [lambda: higher.saveExpressions(lambda exp:self.setExpressions(exp))]
        f = [lambda: higher.toggleExpression(self.expressions, "meow.exp3.json")]
        big = [a]
        event_list = []
        for i in range(5):
            event = Events()
            event_list.append(event)
            ttk.Button(
                root,
                text="Button"+str(i),
                command= lambda  : ConsumerDeque.Consumer(big)
            ).pack(fill="x",side="bottom")
            event.on_change += self.printEvent

        ttk.Button(
            root,
            text="Bind",
            command= lambda : self.helper(event_list, big)
        ).pack(fill="x",side="bottom")

        async_mainloop(root)
    
    def printEvent(self, i):
        print("This was triggered by button",i)

    def helper(self, event_list, big):
        random.choice(event_list).on_change += lambda i: ConsumerDeque.Consumer(big)


if __name__ == "__main__":
    GUI()


