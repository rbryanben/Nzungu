from dotenv import load_dotenv
load_dotenv()

import os
import socketio

sio = socketio.Client()

sio.connect(os.getenv("LIVE_UPDATES_ENDPOINT"),{
    "Authorization" : os.getenv("LIVE_UPDATES_KEY")
})

sio.emit("on-event",{"name" : "ryan"})