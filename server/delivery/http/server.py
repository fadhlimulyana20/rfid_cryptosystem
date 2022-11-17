from flask import Flask
from flask_cors import CORS

class HttpServer():
    app: Flask
    def __init__(self) -> None:
        self.app = Flask(__name__)
        CORS(self.app,resources={r"/*":{"origins":"*"}})
    def register_blueprint(self, blueprint):
        self.app.register_blueprint(blueprint)
    def serve(self):
        self.app.run(debug=True)
    def get_app(self):
        return self.app