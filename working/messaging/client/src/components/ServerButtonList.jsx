import React from 'react';
import ServerButton from './ServerButton';
import { useAllServersState } from '../context/ServerContext';

function ServerButtonList(){
    const { allServersValue } = useAllServersState();
    return(
        <div>
            {allServersValue.map((server) => (
                <ServerButton key={server} port={server}></ServerButton>
            ))}
        </div>
    )
}

export default ServerButtonList;