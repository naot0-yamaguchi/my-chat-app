import os
import redis

import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://redis:6379/0')

from route import create_route
create_route(app, socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
