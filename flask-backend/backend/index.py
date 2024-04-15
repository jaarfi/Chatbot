from flask import Flask, jsonify, request
import pyvts
from . import vts
import asyncio

app = Flask(__name__)


@app.route("/command/flip")
def directflip():
    myvts = vts.vtsconn(pyvts.vts())
    asyncio.run(myvts.connect_auth())
    return asyncio.run(myvts.flip())


@app.route("/<string:Command>")
def flip(Command):
    if request.headers.get("Password") != "examplepass":
        return "Not authorized "
    myvts = vts.vtsconn(pyvts.vts())
    Command.strip()
    asyncio.run(myvts.connect_auth())
    func = getattr(myvts, Command)
    print(func)
    return asyncio.run(func())


@app.route("/<string:Command>/<string:Param>")
def ftwoparter(Command, Param):
    if request.headers.get("Password") != "examplepass":
        return "Not authorized "
    myvts = vts.vtsconn(pyvts.vts())
    Command.strip()
    print(Command)
    print(Param)
    asyncio.run(myvts.connect_auth())
    func = getattr(myvts, Command)
    print(func)
    return asyncio.run(func(Param))
