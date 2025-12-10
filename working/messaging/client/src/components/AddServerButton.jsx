import React, { useState } from 'react';
import { useAllServersState } from '../context/ServerContext';
import Overlay from './Overlay';

function AddServerButton(){
    const { addServer } = useAllServersState();
    const [serverPort, setServerPort] = useState('');
    const [serverName, setServerName] = useState('');
    const [isDisplayed, setIsDisplayed] = useState(false);

    const toggleDisplay = () => {
        setIsDisplayed(!isDisplayed);
    };
    function handleButtonClick(){
        toggleDisplay();
    }
    async function handleAddServer(portOverride){
        const port = portOverride ?? parseInt(serverPort);
        console.log('Adding server:', port);
        const response = await fetch('https://localhost:3002/joinServer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({port: port}),
        });
        const data = await response.json();
        if (data.status === 'success'){
            addServer({serverPort: port, serverName: data.serverName});
            console.log('Server added:', port, data.serverName);
            toggleDisplay();
        }
        else{
            console.log('Server addition failed:', data.serverName);
            toggleDisplay();
        }
    }

    async function handleCreateServer(){
        console.log("creating server:", serverName);
        const response = await fetch('https://localhost:3002/createServer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({serverName: serverName}),
        });
        const data = await response.json();
        if (data.port != null){
            handleAddServer(data.port);
        }
        else{
            console.log('Server addition failed:', serverName);
            toggleDisplay();
        }
    }
    
    return(
        <div style={{gap: '2px'}}>
            <button className="border-2 border-gray-100 rounded-full p-2" onClick={handleButtonClick}>+</button>
            <div style={{display: isDisplayed ? 'block' : 'none'}}>
                <Overlay></Overlay>
                <div style={{zIndex: 1000, position: 'fixed'}}>
                    <button style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-full p-2" onClick={handleAddServer}>+</button>
                    <input style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-md p-2" type="text" placeholder="server port" value={serverPort} onChange={(e) => setServerPort(e.target.value)} />
                    <button style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-full p-2" onClick={handleCreateServer}>+</button>
                    <input style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-md p-2" type="text" placeholder="OR server name (create new server)" value={serverName} onChange={(e) => setServerName(e.target.value)} />
                </div>
            </div>
        </div>
    )
}

export default AddServerButton;