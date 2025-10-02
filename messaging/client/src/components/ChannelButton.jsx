import React from 'react';
import { useChannelState } from '../context/ChannelContext.jsx';

function ChannelButton({ name }) {
    const { updateChannelValue } = useChannelState();
    const handleClick = () => {
        // Remove # prefix when storing in context
        const channelName = name.startsWith('#') ? name.slice(1) : name;
        console.log('Selected channel:', channelName);
        updateChannelValue(channelName);
    }
    
    return(
        <div>
            <button onClick={handleClick}>{name}</button>
        </div>
    )
}

export default ChannelButton;