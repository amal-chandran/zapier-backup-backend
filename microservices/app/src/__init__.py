from flask import Flask

app = Flask(__name__)
# app.config['SECRET_KEY'] = '\x92k\x9c\xb6\x00\xbf^\x01\x07\x94\xff53\x88{\x14\xc0\x19\xdd\x85\x10\xc3\r\x98'    # os.urandom(24)

from .server import *
