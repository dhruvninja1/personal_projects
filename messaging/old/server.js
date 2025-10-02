const express = require('express');
const http = require('http');
const { userInfo } = require('os');
const { Server } = require('socket.io');



const app = express();
app.use(express.static('public')); 

const server = http.createServer(app);
const io = new Server(server, {cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

class messageObject {
    constructor(sender, content, color, timestamp = new Date().toLocaleTimeString()){
        this.sender = sender;
        this.content = content;
        this.color = color
        this.timestamp = timestamp;
    }
}


admin_key = "55twin55"

users={};


io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    socket.on('username message', (msg) =>{
        users[socket.id] = {'username': msg, 'admin' : false, 'muted' : false};
        console.log(socket.id + " : " + users[socket.id].username);
        const joinMessage = new messageObject("System",`${msg} has joined the chat`, "orange");
        io.emit('chat message', joinMessage);
        console.log(users[socket.id])
    });

    socket.on('chat message', (msg) => {
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
                const chatMessage = new messageObject(users[socket.id].username, msg, (users[socket.id].admin ? "red" : "blue"))
                io.emit('chat message', chatMessage);
            }
            else{
                console.log("muted twin");
                personalMutedMessage = new messageObject("System", "you are muted lol", "orange");
                socket.emit('chat message', personalMutedMessage)
            }
        }
 

        
    });

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
        delete users[socket.id];

  });
});


server.listen(14023, () => {
    console.log("Server listening on port 14023");
});