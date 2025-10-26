import React, { useState } from 'react';
import { useSocket } from './socket';
import { useChannelState } from '../context/ChannelContext.jsx';
import { useServerState } from '../context/ServerContext.jsx';

function AddChannelButton(){
    const [channelName, setChannelName] = useState('');
    const { updateChannelValue } = useChannelState();
    const { serverValue } = useServerState();
    const { socket } = useSocket();
    
    function handleAddChannel(){
        if (serverValue == 3000){
            socket.emit('add friend message', channelName);
        }
        else{
            socket.emit('add channel message', channelName);
        }
        setChannelName('');
        updateChannelValue(channelName);
    
    
    }
    
    return(
        <div style={{gap: '2px'}}>
            <button className="border-2 border-gray-100 rounded-full p-2" onClick={handleAddChannel}>+</button>
            <input className="border-2 border-gray-100 rounded-md p-2" type="text" placeholder={serverValue == 3000 ? ("Add email") : ("Channel Name")} value={channelName} onChange={(e) => setChannelName(e.target.value)} />
        </div>
    );
}

export default AddChannelButton;