from delivery.http import server
from delivery.http.handler import hello_world
from delivery.websocket.server import Socket
from delivery.websocket.handler import hello_world as hw_ws
from flask import request
from flask_socketio import emit

if __name__ == "__main__":
    http_server = server.HttpServer()
    http_server.register_blueprint(hello_world.hw)
    # http_server.serve()
    
    socket = Socket(http_server.get_app())
    socket.add_handler(hw_ws.HeloWorldNamespace('/hello'))
    # @socket.socketio.on("connect")
    # def connected():
    #     """event listener when client connects to the server"""
    #     print(request.sid)
    #     print("client has connected")
    #     emit("connect",{"data":f"id: {request.sid} is connected"})
    socket.run(http_server.get_app())
