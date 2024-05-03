import os

from twitchio.ext import commands
from os.path import join, dirname
import consumercoro


class Bot(commands.Bot):

    def __init__(self, trigger_dict):
        self.trigger_dict = trigger_dict

        super().__init__(
            token=os.environ.get("TWITCH_OAUTH_PASS"),
            prefix="!",
            initial_channels=["jaarfi"],
        )

    async def start(self):
        print("im innnnnn")
        await self.connect()
        print("im in")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        first = [i for i in self.trigger_dict.keys() if i in message.content]
        print(first)
        for trigger in first:
            self.trigger_dict[trigger].on_change(message.content)

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def stop(self):
        self._ws.teardown()

    async def event_ready(self):
        print("ready")

    @commands.command(name="test")
    async def my_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def flip(self, ctx: commands.Context):
        # Send a hello back!
        await consumercoro.manager(consumercoro.big)
