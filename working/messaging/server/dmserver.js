const express = require('express');
const https = require('https');
const { Server } = require('socket.io');
const fs = require('fs');

const options = {
    key: fs.readFileSync('../key/192.168.1.172+1-key.pem'),
    cert: fs.readFileSync('../key/192.168.1.172+1.pem')
};

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

const app = express();


const server = https.createServer(options, app);
const io = new Server(server, {cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

class messageObject {
    constructor(sender, content, color, channel='all', timestamp = new Date().toLocaleTimeString()){
        this.sender = sender;
        this.content = content;
        this.channel = channel;
        this.color = color
        this.timestamp = timestamp;
    }
}


function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

function sendAllDataToUser(socket){
    for (let d in data){
        if (d.reciever == users[socket.id].username || d.sender == users[socket.id].username || d.reciever == 'general'){
            socket.emit('chat message', data[d]);
        }
    }
    addChannelMessage = new messageObject("System", 'general', "orange", "all", new Date().toLocaleTimeString());
    socket.emit('add channel message', addChannelMessage);
}

function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}


let users={};
let channels = ['general'];


io.on('connection', (socket) => {
    socket.on('username message', (message) =>{
        msg = message; 
        users[socket.id] = {'username': msg, 'admin' : false, 'muted' : false, 'socket' : socket, 'channels' : ["general"]};
        console.log(socket.id + " : " + users[socket.id].username);
        sendAllDataToUser(socket);
    });

    socket.on('chat message', (message) => {
        const chatMessage = new messageObject(message.sender, message.content, "blue", message.reciever);
        if (!(users[socket.id].channels.includes(chatMessage.channel))){
            users[socket.id].channels.push(chatMessage.channel);
        }
        console.log(chatMessage);
        data.push(chatMessage);
        saveData(data);
        for (let socketID in users){
            var user = users[socketID];
            if (user.username === chatMessage.channel || user.username == chatMessage.sender || chatMessage.channel == "general"){
                tempSocket = user.socket;
                if (user.username != chatMessage.sender && chatMessage.channel !== 'general'){
                    if (!(user.channels.includes(chatMessage.sender))){
                        user.channels.push(chatMessage.sender);
                        addChannelMessage = new messageObject("System", chatMessage.sender, "orange", "all", new Date().toLocaleTimeString());
                        tempSocket.emit('add channel message', addChannelMessage);
                    }
                }
                tempSocket.emit('chat message', chatMessage);
                console.log("emmitiing mesg");
            }
        }
    });

    socket.on('disconnect', () => {
        delete users[socket.id];
    });

    socket.on('add friend message', (msg) => {
        addChannelMessage = new messageObject("System", msg, "orange", "all", new Date().toLocaleTimeString());
        socket.emit('add channel message', addChannelMessage);
    });
});


server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server listening on port ${PORT}`);
});
