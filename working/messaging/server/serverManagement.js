const { randomInt } = require('crypto');
const express = require('express');
const app = express();
const { exec } = require('child_process');
const cors = require('cors');
const PORT = 3002;
app.use(cors());
app.use(express.json());
openServers={3000: "test", 434: "test2"};

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

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});