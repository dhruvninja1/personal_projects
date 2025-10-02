import React, { useEffect, useState } from 'react';
import UserLabel from './UserLabel';
import { useSocket } from './socket';

function UserList(){
    const [users, setUsers] = useState([]);
    const { socket } = useSocket();
    
    useEffect(() => {
        if (!socket) return;
        socket.on('user list', (userList) => {
            console.log('Received user list:', userList);
            setUsers(userList);
        });
        
        return () => {
            socket.off('user list');
        };
    }, [socket]);
    
    return(
        <div className='w-48 border-2 border-gray-300 rounded-md p-2'>
            <h3 className='font-bold mb-2'>Users ({users.length})</h3>
            {users.map((username, index) => (
                <UserLabel key={index} username={username}></UserLabel>
            ))}
        </div>
    )
}


export default UserList;