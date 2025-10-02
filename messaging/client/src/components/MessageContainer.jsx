import React, { useState, useEffect } from 'react';
import Message from './Message'
import MessageForm from './MessageForm'
import { useSocket } from './socket'
import { useChannelState } from '../context/ChannelContext.jsx';

function MessageContainer(){
    const [messages, setMessages] = useState([
        { id: 1, sender: "System", content: "Connection is pending...", timestamp: new Date().toLocaleTimeString(), color: "orange"},
    ]);
    const { socket } = useSocket();
    const { channelValue } = useChannelState();
    
    useEffect(() => {
        if (!socket) return;
        const handleNewMessage = (newMessage) => {
            setMessages(prevMessages => [
                ...prevMessages, 
                {...newMessage, id: Date.now()} 
            ]);
        };

        socket.on('chat message', handleNewMessage);
        
        return () => {
            socket.off('chat message', handleNewMessage);
        };
    }, [socket]);
    return(
        <div>
            <div className='h-[90vh] w-[70vw] overflow-y-auto border-2 border-gray-300 rounded-md p-2'>
                {messages.map((msg, index) => 
                    msg.channel === channelValue || msg.channel === 'all' ? (
                    <Message
                        key={msg.id}
                        sender={index === 0 || messages[index - 1].sender !== msg.sender ? msg.sender : null}          
                        content={msg.content}
                        timestamp={msg.timestamp}
                        color={msg.color}>
                    </Message>
                    ) : null
                )}
            </div>
            <MessageForm></MessageForm>
        </div>
    )
}

export default MessageContainer;