from flask_socketio import Namespace, emit

class HeloWorldNamespace(Namespace):
    def on_connect(self):
        print("Connected")
        emit('my response', {'data': 'Connected'})

    def on_disconnect(self):
        print("Disconnected")
        emit('my response', {'data': 'Disconnected'})