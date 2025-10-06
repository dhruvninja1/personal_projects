const { randomInt } = require('crypto');
const express = require('express');
const app = express();
const { exec } = require('child_process');
const PORT = 3002;
app.use(express.json());
openServers={};


app.post('/createServer', (req, res) => {
    data = req.body;
    serverName = req['name'];
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
    port = body['port'];
    if (port in openServers){
        res.json({status: 'success', serverName: openServers[port]});
    }
    else{
        res.json({status: 'failure', serverName: null});
    }
});