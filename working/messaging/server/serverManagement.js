const { randomInt } = require('crypto');
const express = require('express');
const app = express();
const { exec } = require('child_process');
const kill = require('kill-port');
const cors = require('cors');
const fs = require('fs');
const PORT = 3002;

serverDataFile = "./data/openservers.json"; 

const https = require('https');
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

openServers = JSON.parse(fs.readFileSync(serverDataFile, "utf8"));
console.log(openServers);

const options = {
    key: fs.readFileSync('../key/192.168.1.172+1-key.pem'),
    cert: fs.readFileSync('../key/192.168.1.172+1.pem')
};

userDataFile = "data/userData.json";
users = JSON.parse(fs.readFileSync(userDataFile, "utf8"));




exec(`node dmserver.js`)
for (const server of openServers){
    exec(`node server.js ${server.port} ${server.name}`);
}

function cleanup(){
    for (const server of openServers){
        kill(server.port, 'tcp');
    }
    kill(3002, 'tcp');
}

app.post('/createServer', (req, res) => {
    data = req.body;
    serverName = data.serverName;
    testport = randomInt(50000, 50500);
    
    // Find a unique port that doesn't exist in openServers
    let portExists = true;
    while (portExists) {
        portExists = openServers.some(server => server.port === testport);
        if (portExists) {
            testport = randomInt(50000, 50500);
        }
    }
    
    exec(`node server.js ${testport} ${serverName}`);
    res.json({port : testport});
    
    // Add new server to the array
    openServers.push({ name: serverName, port: testport });
    fs.writeFileSync(serverDataFile, JSON.stringify(openServers, null, 4));
    console.log(data);
    console.log(openServers);
});

app.post('/joinServer', (req, res) => {
    body = req.body;
    port = parseInt(body.port);
    
    // Find the server with matching port in the array
    const server = openServers.find(server => server.port === port);
    
    if (server) {
        res.json({status: 'success', serverName: server.name});
    } else {
        res.json({status: 'failure', serverName: null});
    }
});

app.post('/createUser', (req, res) => {
    body = req.body;
    users[body.email] = body.username;
    console.log("GOT USER " + body.email + " USERNAME: " + body.username);
    console.log(users);
    fs.writeFileSync(userDataFile, JSON.stringify(users, null, 2));
    res.json({status: "success"});
});

app.post('/addFriend', (req, res) => { 
    body = req.body;
    if (users[body.email]){
        res.json({status : "success", username : users[body.email]});
    }
    else{
        res.json({status : 'fail', username : undefined});
    }
});

server = https.createServer(options, app);

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server listening on port ${PORT}`);
    
});

process.on('SIGINT', cleanup); 
process.on('SIGTERM', cleanup);