document.addEventListener('DOMContentLoaded', () => {
  const socket = io();
  const username = prompt('Enter your name');
  const room = prompt('Enter room name to join');
  
  socket.emit('join', {username: username, room: room});
  
  socket.on('history', history => {
    const chatWindow = document.querySelector('.chat-window');
    history.forEach(msg => {
      addMessage(msg, 'received');
    });
  });
  
  document.querySelector('.chat-input button').addEventListener('click', () => {
    const message = document.querySelector('.chat-input textarea').value;
    if (message) {
      socket.emit('message', {room: room, message: message});
      addMessage(message, 'sent');
      document.querySelector('.chat-input textarea').value = '';
    }
  });
  
  socket.on('message', msg => addMessage(msg, 'received'));
  
  socket.on('join_message', msg => addMessage(msg, 'join'));
});

function addMessage(msg, className) {
  const chatWindow = document.querySelector('.chat-window');
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', className);
  const contentDiv = document.createElement('div');
  contentDiv.classList.add('content');
  contentDiv.textContent = msg;
  messageDiv.appendChild(contentDiv);
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
