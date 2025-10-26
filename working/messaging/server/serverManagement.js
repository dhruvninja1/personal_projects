const { randomInt } = require('crypto');
const express = require('express');
const app = express();
const { exec } = require('child_process');
const cors = require('cors');
const fs = require('fs');
const PORT = 3002;
app.use(cors());
app.use(express.json());
openServers={3000: "dms", 434: "test"};

userDataFile = "userData.json";
users = JSON.parse(fs.readFileSync(userDataFile, "utf8"));
console.log(users);

app.post('/createServer', (req, res) => {
    data = req.body;
    serverName = body.serverName;
    testport = randomInt(50000, 50500);
    while (testport in openServers){
        testport = randomInt(50000, 50500);
    }
    exec(`node server.js ${testport} ${serverName}`);
    res.send(testport);
    openServers[testport] = serverName;

});

app.post('/joinServer', (req, res) => {
    body = req.body;
    console.log(req);
    port = body.port;
    if (port in openServers){
        res.json({status: 'success', serverName: openServers[port]});
    }
    else{
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

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});