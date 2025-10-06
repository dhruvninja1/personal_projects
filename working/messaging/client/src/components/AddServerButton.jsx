import React, { useState } from 'react';
import { useAllServersState } from '../context/ServerContext';

function AddServerButton(){
    const { addServer } = useAllServersState();
    const [serverName, setServerName] = useState('');
    function handleAddChannel(){
        addServer(serverName);
        console.log('Server added:', serverName);
    }
    
    return(
        <div style={{gap: '2px'}}>
            <button className="border-2 border-gray-100 rounded-full p-2" onClick={handleAddChannel}>+</button>
            <input className="border-2 border-gray-100 rounded-md p-2" type="text" placeholder="server port" value={serverName} onChange={(e) => setServerName(e.target.value)} />
        </div>
    )
}

export default AddServerButton;