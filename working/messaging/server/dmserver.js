const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');


const PORT = 3000;
const NAME = dms
dataPath =`./data/${NAME}-${PORT}.json`;

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
        if (d.reciever == users[socket.id][username]){
            socket.emit('chat message', data[d]);
        }
    }
}

function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}



users={};
channels=['general'];


io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    socket.on('username message', (message) =>{

    });

    socket.on('chat message', (message) => {
    });


    socket.on('add friend message', (msg) => {
    
    });

    socket.on('disconnect', () => {
  });
});


server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
