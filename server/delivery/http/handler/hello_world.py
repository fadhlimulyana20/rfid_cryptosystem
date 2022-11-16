from flask import Blueprint
import json

hw = Blueprint('hello_world', __name__)

@hw.route('/', methods=['GET'])
def hello_world():
    return {"hello": "world"}