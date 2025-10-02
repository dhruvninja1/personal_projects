import React from 'react';
import { useChannelState } from '../context/ChannelContext.jsx';

function ChannelButton({ name }) {
    const { updateChannelValue, channelValue } = useChannelState();
    const handleClick = () => {
        console.log('Selected channel:', name);
        updateChannelValue(name);
    }
    const textColor = name === `${channelValue}` ? 'text-green-700' : 'text-gray-500';

    return(
        <div>
            <button onClick={handleClick} className={`${textColor}`}>{name}</button>
        </div>
    )
}

export default ChannelButton;