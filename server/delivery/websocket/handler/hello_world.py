from flask_socketio import Namespace, emit
from flask import request

class HeloWorldNamespace(Namespace):
    def on_connect(self):
        print(request.sid)
        print("client has connected")
        emit("connect",{"data":f"id: {request.sid} is connected"})

    def on_disconnect(self):
        print("Disconnected")
        emit('my response', {'data': 'Disconnected'})