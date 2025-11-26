import React, { useState, useEffect } from 'react';
import { useSocket } from './socket';
import ChannelButton from './ChannelButton';
import AddChannelButton from './AddChannelButton';
import { useServerState } from '../context/ServerContext.jsx';

function ChannelList(){
    const [messages, setMessages] = useState([]);
    const { socket, isConnected } = useSocket();
    const { serverValue } = useServerState();
    
    // Clear channels when server changes
    useEffect(() => {
        setMessages([]);
    }, [serverValue]);
    
    useEffect(() => {
        if (!socket){ console.log('bug'); return;}
        
        const handleNewMessage = (newMessage) => {
            console.log("got channel" + newMessage.content);
            setMessages(prevMessages => [
                ...prevMessages,
                {...newMessage, id: Date.now()} 
            ]);
        };
        
        const handleConnect = () => {
            console.log("IMPORTANT connected to server");
        };
        
        console.log(socket);
        
        // Check if already connected
        if (socket.connected) {
            console.log("IMPORTANT connected to server (already connected)");
        }
        
        socket.on('connect', handleConnect);
        socket.on('add channel message', handleNewMessage);
        console.log("listening to add channel message");
        
        return () => {
            socket.off('connect', handleConnect);
            socket.off('add channel message', handleNewMessage);
        };
    }, [socket, serverValue, isConnected]);
    return(
        <div className='p-2'>
            <div>
                <AddChannelButton></AddChannelButton>
            </div>
            <div>
                {messages.map((msg, index) => (
                    <ChannelButton 
                        key={index}
                        name={serverValue == 3000 ? `${msg.content}` : `#${msg.content}`}>
                    </ChannelButton>
                ))}
            </div>
        </div>
    )
}


export default ChannelList;