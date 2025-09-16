import socketio
import os , logging

class Helper:
    def __init__(self):
        self.client = socketio.Client()
        self.endpoint = os.getenv("LIVE_UPDATES_ENDPOINT")
        self.ensure_connection()
        
    def ensure_connection(self,timeout=5):
        # Return if connected
        if self.client.connected:
            return
        
        try:
            self.client.connect(self.endpoint,{
                "Authorization" : os.getenv("LIVE_UPDATES_KEY")
            },wait_timeout=timeout)
        except Exception as e:
            logging.error(f"Failed to connect to socket.io {self.endpoint} - {e}")
        
            
instance = Helper()
