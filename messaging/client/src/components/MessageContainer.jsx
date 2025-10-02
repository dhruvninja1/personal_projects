import React, { useState, useEffect } from 'react';
import Message from './Message'
import MessageForm from './MessageForm'
import { useSocket } from './socket'

function MessageContainer(){
    const [messages, setMessages] = useState([
        { id: 1, sender: "System", content: "Connection is pending...", timestamp: new Date().toLocaleTimeString(), color: "orange"},
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

        socket.on('chat message', handleNewMessage);
        
        return () => {
            socket.off('chat message', handleNewMessage);
        };
    }, [socket]);
    return(
        <div>
            <div>
                {messages.map((msg, index) => (
                    <Message
                        key={msg.id}
                        sender={index === 0 || messages[index - 1].sender !== msg.sender ? msg.sender : null}          
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