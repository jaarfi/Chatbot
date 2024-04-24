from irc.bot import SingleServerIRCBot
import irc.client
import random
import re
import os
import asyncio
import Jaarfivts.jaarfivts as jaarfivts
from events import Events

server = "irc.chat.twitch.tv"
port = 6667
resturl = "http://127.0.0.1:5000"

command_list = ["bot","fuck"]

def cleanString(message: str):
    return re.compile("[\W_]+", re.UNICODE).sub("", message)


class Tmi(SingleServerIRCBot):
    def __init__(self, username, password, channel, message_handler, trigger_dict):
        self.channel = "#" + channel
        self.message_handler = message_handler
        self.trigger_dict = trigger_dict

        super().__init__([(server, port, password)], username, username)

    def on_welcome(self, client, _):
        client.cap("REQ", ":twitch.tv/membership")
        client.cap("REQ", ":twitch.tv/tags")
        client.cap("REQ", ":twitch.tv/commands")
        client.join(self.channel)
        client.privmsg(self.channel, "Bot is live")

    def on_pubmsg(self, client, message):
        response = self.message_handler(message)

        if response:
            print(response)
            client.privmsg(self.channel, response)


def start_bot(parse_message, trigger_dict):
    channel = "jaarfi"
    username = "jaarfibot"
    password = "oauth:" + os.environ.get("TWITCH_OAUTH_PASS")

    bot = Tmi(username, password, channel, parse_message, trigger_dict)
    bot.start()


def message_handler(msg: irc.client.Event):
    chat_message = msg.arguments[0]
    tags = {item["key"]: item["value"] for item in msg.tags}

    trigger, *args = str.split(chat_message)

    command = None
    if trigger.startswith("!"):
        command = trigger[1:]
    else:
        if trigger in command_list and args:
            command = args[0]
        if trigger in trigger_dict.keys():
            trigger_dict[trigger].on_change(args)

    if not command:
        return
    
    if command == "d":
        return dice(args)
    
    if command == "add":
        return addPrintToTrigger(args, trigger_dict)
        
    return

def dice(args):
    if args and args[0].isdigit():
        return "You rolled a {}".format(random.randint(1, int(args[0])))
    return "Usage: !d 'number' to roll a dice with 'number' sides"
    
def addPrintToTrigger(args, trigger_dict):
    if not args:
        return "Usage: !add 'word' to print the message if its preceded by 'word'"
    event = Events()
    trigger_dict[args[0]] = event
    event.on_change += printTriggerSource
    return f"Added {args[0]} so that it triggers a print"


def printTriggerSource(source):
    print(source)

event = Events()
trigger_dict = {"print":event}
event.on_change += printTriggerSource
start_bot(message_handler, trigger_dict)



"!command arg1 arg2 arg3 arg4"

"!command as group1"
"arg1 as group2"
"arg2 as group3"
"arg3 as group4"
"arg4 as group5"

"[command, 'arg1, arg2, arg3', arg3]"