const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');


const PORT = process.argv[2];
const NAME = process.argv[3];
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

function sendAllData(socket){
    for (let d in data){
        socket.emit('chat message', data[d]);
    }
}
function saveData(data){
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

function sendAllData(socket){
    for (let d in data){
        socket.emit('chat message', data[d]);
    }
}

admin_key = "55twin55"

users={};
channels=['general'];


io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    socket.on('username message', (message) =>{
        msg = message; 
        users[socket.id] = {'username': msg, 'admin' : false, 'muted' : false};
        console.log(socket.id + " : " + users[socket.id].username);
        console.log(users[socket.id])
        for (let c in channels){
            const joinChannelMessage = new messageObject("System",`${channels[c]}`, "orange");
            socket.emit('add channel message', joinChannelMessage);
        }
        
        temp = [];
        for (let u in users){
            temp.push(users[u].username);
        }
        io.emit('user list', temp);
        sendAllData(socket);
    });

    socket.on('chat message', (message) => {
        msg = message.message;
        console.log(users[socket.id]);
        if (msg == admin_key){
            users[socket.id].admin = true;
        }
        

        else{
            if (msg.includes("/mute") && users[socket.id].admin){
                temp = msg.slice(6);
                for (let t in users){
                    if (users[t].username == temp && !users[t].admin){
                        users[t].muted = true;
                        const globalMuteMessage = new messageObject("System", `${users[t].username} has been muted.`, "orange")
                        io.emit('chat message', globalMuteMessage);
                    } 
                };
            }
            else if (msg.includes("/unmute") && users[socket.id].admin){
                temp = msg.slice(8);
                for (let t in users){
                    if (users[t].username == temp && !users[t].admin){
                        users[t].muted = false;
                        const globalMuteMessage = new messageObject("System", `${users[t].username} has been unmuted.`, "orange")
                        io.emit('chat message', globalMuteMessage);
                    } 
                };
            }
            else if (!users[socket.id].muted){
                const chatMessage = new messageObject(users[socket.id].username, msg, (users[socket.id].admin ? "red" : "blue"), message.channel)
                data.push(chatMessage);
                saveData(data);
                io.emit('chat message', chatMessage);
            }
            else{
                console.log("muted twin");
                personalMutedMessage = new messageObject("System", "you are muted lol", "orange");
                socket.emit('chat message', personalMutedMessage)
            }
        }
 

        
    });


    socket.on('add channel message', (msg) => {
        console.log(msg);
        addChannelMessage = new messageObject("System", msg, "orange", "all", new Date().toLocaleTimeString());
        io.emit('add channel message', addChannelMessage);
        channels.push(msg);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
        delete users[socket.id];
        temp = [];
        for (let u in users){
            temp.push(users[u].username);
        }
        io.emit('user list', temp);

  });
});


server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
