import socketio
import os , logging

class Helper:
    def __init__(self):
        self.client = socketio.Client()
        self.endpoint = os.getenv("LIVE_UPDATES_ENDPOINT")
        
        try:
            self.client.connect(self.endpoint,{
                "Authorization" : os.getenv("LIVE_UPDATES_KEY")
            })
        except Exception as e:
            logging.error(f"Failed to connect to socket.io {self.endpoint} - {e}")
            raise Exception(f"Failed to connect to socket.io {self.endpoint} - {e}")
            
instance = Helper()