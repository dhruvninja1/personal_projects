import React, { useState, useEffect } from 'react';
import Message from './Message'
import MessageForm from './MessageForm'
import { useSocket } from './socket'
import { useChannelState } from '../context/ChannelContext.jsx';
import { useServerState } from '../context/ServerContext.jsx';

function MessageContainer(){
    const [messages, setMessages] = useState([
        { id: 1, sender: "System", content: "Connection is pending...", timestamp: new Date().toLocaleTimeString(), color: "orange"},
    ]);
    const { socket } = useSocket();
    const { channelValue } = useChannelState();
    const { serverValue } = useServerState();
    
    // Clear messages when server changes
    useEffect(() => {
        setMessages([
            { id: 1, sender: "System", content: "Connection is pending...", timestamp: new Date().toLocaleTimeString(), color: "orange"},
        ]);
    }, [serverValue]);
    
    useEffect(() => {
        if (!socket) return;
        
        const handleNewMessage = (newMessage) => {
            setMessages(prevMessages => [
                ...prevMessages, 
                {...newMessage, id: Date.now()} 
            ]);
            console.log(newMessage);
        };

        // Remove any existing listeners first
        socket.off('chat message', handleNewMessage);
        socket.on('chat message', handleNewMessage);
        
        return () => {
            socket.off('chat message', handleNewMessage);
        };
    }, [socket]);
    // Filter messages for current channel first
    const filteredMessages = messages.filter(msg => 
        msg.channel === channelValue || msg.channel === 'all' || msg.sender === channelValue
    );

    return(
        <div>
            <div className='h-[90vh] w-[70vw] overflow-y-auto border-2 border-gray-300 rounded-md p-2'>
                {filteredMessages.map((msg, index) => (
                    <Message
                        key={index}
                        sender={index === 0 || filteredMessages[index - 1].sender !== msg.sender ? msg.sender : null}          
                        content={msg.content}
                        timestamp={msg.timestamp}
                        color={msg.color}>
                    </Message>
                ))}
            </div>
            <MessageForm></MessageForm>
        </div>
    )
}

export default MessageContainer;