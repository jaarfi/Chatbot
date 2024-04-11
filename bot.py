from irc.bot import SingleServerIRCBot
import irc.client
import random
import pyttsx3
from openai import OpenAI
import re
import pyvts
import asyncio
import os
import vts

server = 'irc.chat.twitch.tv'
port = 6667


class Tmi(SingleServerIRCBot):
    def __init__(self, username, password, channel, message_handler, tts):
        self.channel = '#' + channel
        self.message_handler = message_handler
        self.tts = tts

        super().__init__([(server, port, password)], username, username)
    
    def on_welcome(self, client, _):
        client.cap('REQ', ':twitch.tv/membership')
        client.cap('REQ', ':twitch.tv/tags')
        client.cap('REQ', ':twitch.tv/commands')
        client.join(self.channel)
        client.privmsg(self.channel, "Bot is live")
    
    def on_pubmsg(self, client, message):
        response = self.message_handler(message, self.tts)

        if response:
            response = "Bot: " + response
            print(response)
            client.privmsg(self.channel, response)

def start_bot(parse_message, tts):
    channel = "jaarfi"
    username = "jaarfibot"
    password = "oauth:" + os.environ.get("TWITCH_OAUTH_PASS")

    bot = Tmi(username, password, channel, parse_message, tts)
    bot.start()

def message_handler(msg: irc.client.Event, tts: pyttsx3.Engine):
    chat_message = msg.arguments[0]
    tags = {item['key']:item['value'] for item in msg.tags}

    if not chat_message.startswith('!'):
        return

    chat_message = chat_message[1:]
    if chat_message.startswith('d'):
        chat_message = chat_message[1:]
        if chat_message.isdigit():
            return 'You rolled a {}'.format(random.randint(1, int(chat_message)))

    if chat_message.startswith('tts') and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[3:]
        engine.say(chat_message)
        engine.runAndWait()
    
    if chat_message.startswith('gpt') and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[3:]
        
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a twitch chatbot, answering questions in text-to-speech. Do not use any profane language. You answer questions as though you are a real person with opinions"},
            {"role": "user", "content": "Whats your favorite anime?"},
            {"role": "assistant", "content": "That's obviously Tengen Toppa Gurren Lagann."},
            {"role": "user", "content": chat_message}
        ]
        )
        tts.say(response.choices[0].message.content)
        tts.runAndWait()
        return response.choices[0].message.content

    if chat_message.startswith('flip'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[4:]
        asyncio.run(vts.flip(myvts))

    if chat_message.startswith('slideright'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[4:]
        asyncio.run(vts.slideright(myvts))

    if chat_message.startswith('zoomin'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[4:]
        asyncio.run(vts.zoomin(myvts))

    if chat_message.startswith('items'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[4:]
        asyncio.run(vts.getItems(myvts))

    if chat_message.startswith('pat'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[3:]
        if chat_message.isdigit():
           asyncio.run(vts.toggleHeadpat(myvts, int(chat_message)))

    if chat_message.startswith('turbopat'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[8:]
        if chat_message.isdigit():
           asyncio.run(vts.turboHeadpat(myvts, int(chat_message)))

    if chat_message.startswith('moustache'):# and tags['display-name'] == 'jaarfi':
        chat_message = chat_message[9:]
        asyncio.run(vts.zoomMoustache(myvts))
    return



engine = pyttsx3.init()
print(engine.getProperty('voice'))
engine.setProperty('voice', engine.getProperty('voices')[0].id)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

myvts  = pyvts.vts()
asyncio.run(vts.connect_auth(myvts))

start_bot(message_handler, engine)