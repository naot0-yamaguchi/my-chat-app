from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

def create_route(app: Flask, socketio: SocketIO):

    from __init__ import redis_client

    def get_chat_history(room):
        return redis_client.lrange(f'chat_history:{room}', 0, -1)

    def save_chat_message(room, message):
        redis_client.rpush(f'chat_history:{room}', message)

    @app.get('/')
    def index():
        return render_template('index.html')

    @socketio.on('join')
    def on_join(data):
        username = data['username']
        room = data['room']
        join_room(room)
        history = get_chat_history(room)
        socketio.emit('history', history, to=request.sid)
        socketio.emit('join_message', f'{username} has entered the room.', to=room)

    @socketio.on('leave')
    def on_leave(data):
        username = data['username']
        room = data['room']
        leave_room(room)
        socketio.emit('message', f'{username} has left the room.', to=room)

    @socketio.on('message')
    def handle_message(data):
        room = data['room']
        msg = data['message']
        save_chat_message(room, msg)
        socketio.emit('message', msg, to=None, include_self=False)
