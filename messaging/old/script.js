username=""
userNameInputButton = document.getElementById("userNameInputButton");
popup = document.getElementById("popup");
overlay = document.getElementById("overlay");




const socket = io("http://localhost:14023");
const form = document.getElementById('form');
const input = document.getElementById('input');
const messages = document.getElementById('messages');

userNameInputButton.addEventListener('click', function(){
    usernameInputField = document.getElementById("usernameInputField");
    username = usernameInputField.value;
    popup.style.display='none';
    overlay.style.display='none';
    console.log(username);
    socket.emit('username message', username);
});


socket.on('connect', () => {
  console.log('Connected to Socket.IO server with ID:', socket.id);
});


form.addEventListener('submit', function(e) {
    e.preventDefault();
    if (input.value){
        socket.emit('chat message', input.value);
        input.value = '';
    }
});

socket.on('chat message', function(msg){
    const item = document.createElement('li');
    const senderSpan = document.createElement('span');
    const contentSpan = document.createElement('span');

    senderSpan.style.color = msg.color; 
    
    if (msg.content.includes(`@${username}`)){
        contentSpan.style.backgroundColor = 'yellow';
    }
    senderSpan.textContent = `${msg.sender}: `;
    contentSpan.textContent = msg.content;

    item.appendChild(senderSpan);
    item.appendChild(contentSpan);
    messages.append(item);
    
    window.scrollTo(0, document.body.scrollHeight);
});





