import { useSocket } from "./socket";
import React, { useState } from 'react';
import data from '@emoji-mart/data'
import Picker from '@emoji-mart/react'
import { useChannelState } from '../context/ChannelContext.jsx';

function MessageForm(){
    const [msg, setMsg] = useState('');
    const [isEmojiPickerOpen, setIsEmojiPickerOpen] = useState(false); 
    const { socket, isConnected } = useSocket();
    const { channelValue } = useChannelState();
    
    const handleSubmit = (event) => {
        event.preventDefault(); 
        console.log('Form submitted with name:', msg);
        setMsg('');
        socket.emit('chat message', {'message': msg, 'channel': channelValue});
    };
    
    const handleSelect = (emoji) => {
        setMsg(msg + emoji.native);
        setIsEmojiPickerOpen(false);
    };
    
    const handleEmojiToggle = () => {
        setIsEmojiPickerOpen(!isEmojiPickerOpen);
    };
    
    return (
        <div className="relative">
            {isEmojiPickerOpen && ( 
                <div className="absolute bottom-full mb-2 z-50 right-0">
                    <Picker data={data} onEmojiSelect={handleSelect} />
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={msg}
                    onChange={(e) => setMsg(e.target.value)}
                    className="border-2 border-gray-300 rounded-md p-2 w-5/6">
                </input>
                <button type="button" onClick={handleEmojiToggle} className="rounded-md p-2 text-2xl">😀</button> 
                <button type="submit" className="text-2xl">☝</button>
            </form>
            
        </div>
    )
}

export default MessageForm;