const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');


const PORT = 3000;
const NAME = 'dms'
let dataPath =`./data/${NAME}-${PORT}.json`;

try{
    data = JSON.parse(fs.readFileSync(dataPath, "utf8"));
}
catch(e){
    data = [];
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

console.log(data);
const app = express();


const server = http.createServer(app);
const io = new Server(server, {cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

class DMObject {
    constructor(sender, reciever, content, timestamp = new Date().toLocaleTimeString()){
        this.sender = sender;
        this.content = content;
        this.reciever = reciever;
        this.timestamp = timestamp;
    }
}

function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

function sendAllDataToUser(socket){
    for (let d in data){
        if (d.reciever == users[socket.id].username){
            socket.emit('chat message', data[d]);
        }
    }
}

function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}


let users={};
let channels=['general'];


io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);
    socket.on('username message', (message) =>{
        msg = message; 
        users[socket.id] = {'username': msg, 'admin' : false, 'muted' : false, 'socket' : socket};
        console.log(socket.id + " : " + users[socket.id].username);
        sendAllDataToUser(socket);
    });

    socket.on('chat message', (message) => {
        const chatMessage = new DMObject(message.sender, message.reciever, message.content);
        data.push(chatMessage);
        saveData(data);
        for (let user in users){
            if (user.username === chatMessage.reciever || user.username == chatMessage.sender){
                tempSocket = user.socket;
                tempSocket.emit('chat message', chatMessage);
            }
        }
    });

    socket.on('disconnect', () => {
        delete users[socket.id];
    });
});


server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
