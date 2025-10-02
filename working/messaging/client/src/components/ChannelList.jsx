import React, { useState, useEffect } from 'react';
import { useSocket } from './socket';
import ChannelButton from './ChannelButton';
import AddChannelButton from './AddChannelButton';

function ChannelList(){
    const [messages, setMessages] = useState([
    ]);
    const { socket } = useSocket();
    
    useEffect(() => {
        if (!socket) return;
        const handleNewMessage = (newMessage) => {
            setMessages(prevMessages => [
                ...prevMessages, 
                {...newMessage, id: Date.now()} 
            ]);
        };

        socket.on('add channel message', handleNewMessage);
        
        return () => {
            socket.off('add channel message', handleNewMessage);
        };
    }, [socket]);
    return(
        <div className='p-2'>
            <div>
                <AddChannelButton></AddChannelButton>
            </div>
            <div>
                {messages.map((msg, index) => (
                    <ChannelButton 
                        key={index}
                        name={`#${msg.content}`}>
                    </ChannelButton>
                ))}
            </div>
        </div>
    )
}


export default ChannelList;