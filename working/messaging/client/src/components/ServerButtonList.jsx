import React from 'react';
import ServerButton from './ServerButton';
import { useAllServersState } from '../context/ServerContext';
import AddServerButton from './AddServerButton';

function ServerButtonList(){
    const { allServersValue } = useAllServersState();
    return(
        <div>
            <div>
                {allServersValue.map((server) => (
                    <ServerButton key={server} port={server}></ServerButton>
                ))}
            </div>
            <AddServerButton></AddServerButton>
        </div>
    )
}

export default ServerButtonList;