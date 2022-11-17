from delivery.http import server
from delivery.http.handler import hello_world
from delivery.websocket.server import Socket
from delivery.websocket.handler import hello_world as hw_ws

if __name__ == "__main__":
    http_server = server.HttpServer()
    http_server.register_blueprint(hello_world.hw)
    http_server.serve()
    
    socket = Socket(http_server.get_app())
    socket.run(http_server.get_app())
    socket.add_handler(hw_ws.HeloWorldNamespace)