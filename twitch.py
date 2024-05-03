from twitchio.ext import commands
import os
import consumercoro
from threading import Thread


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(
            token=os.environ.get("TWITCH_OAUTH_PASS"),
            prefix="!",
            initial_channels=["jaarfi"],
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        await self.connected_channels[0].send(message.content)

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def flip(self, ctx: commands.Context):
        # Send a hello back!
        await consumercoro.manager(consumercoro.big)


def start():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    start()
