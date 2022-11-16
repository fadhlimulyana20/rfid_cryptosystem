from delivery.http import server
from delivery.http.handler import hello_world

if __name__ == "__main__":
    http_server = server.HttpServer()
    http_server.register_blueprint(hello_world.hw)
    http_server.serve()