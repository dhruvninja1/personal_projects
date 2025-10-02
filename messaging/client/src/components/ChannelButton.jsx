import React, { useState } from 'react';
import { useChannelState } from '../context/ChannelContext.jsx';


function ChannelButton({ name }) {
    const { updateChannelValue, channelValue } = useChannelState();
    const updateChannel = () => {
        updateChannelValue(name);
        console.log(channelValue);
    }
    return(
        <div>
            <button onClick={updateChannel}>{name}</button>
        </div>
    )
}

export default ChannelButton;