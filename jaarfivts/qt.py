async def trigger_hotkey(animation):
    global myvts
    if not myvts.websocket.open:
        print("Connection to VTube Studio is closed. Trying to reconnect...")
        await connect_auth()
    try:
        send_hotkey_request = myvts.vts_request.requestTriggerHotKey(animation)
        await myvts.request(send_hotkey_request)
    except websockets.exceptions.ConnectionClosedError:
        print(
            "Failed to send request to VTube Studio because the connection was closed."
        )
