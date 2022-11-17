from flask import Flask

class HttpServer():
    app: Flask
    def __init__(self) -> None:
        self.app = Flask(__name__)
    def register_blueprint(self, blueprint):
        self.app.register_blueprint(blueprint)
    def serve(self):
        self.app.run(debug=True)
    def get_app(self):
        return self.app