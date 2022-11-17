from flask_socketio import SocketIO
from flask import Flask

class Socket():
    def __init__(self, app: Flask) -> None:
        self.socketio = SocketIO(app=app, cors_allowed_origins="*")

    def run(self, app: Flask):
        self.socketio.run(app=app)
    
    def add_handler(self, handler):
        self.socketio.on_namespace(handler)