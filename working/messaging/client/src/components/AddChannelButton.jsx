import React, { useState } from 'react';
import { useSocket } from './socket';
import { useChannelState } from '../context/ChannelContext.jsx';

function AddChannelButton(){
    const [channelName, setChannelName] = useState('');
    const { updateChannelValue } = useChannelState();
    const { socket } = useSocket();
    
    function handleAddChannel(){
        socket.emit('add channel message', channelName);
        setChannelName('');
        updateChannelValue(channelName);
    }
    
    return(
        <div>
            <button onClick={handleAddChannel}>+</button>
            <input type="text" placeholder="Channel Name" value={channelName} onChange={(e) => setChannelName(e.target.value)} />
        </div>
    )
}

export default AddChannelButton;