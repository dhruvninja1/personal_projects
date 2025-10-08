import React, { useState } from 'react';
import { useAllServersState } from '../context/ServerContext';
import Overlay from './Overlay';

function AddServerButton(){
    const { addServer } = useAllServersState();
    const [serverPort, setServerPort] = useState('');
    const [isDisplayed, setIsDisplayed] = useState(false);

    const toggleDisplay = () => {
        setIsDisplayed(!isDisplayed);
    };
    function handleButtonClick(){
        toggleDisplay();
    }
    function handleAddServer(){

        addServer(serverPort);
        console.log('Server added:', serverPort);
        toggleDisplay();
    }
    
    return(
        <div style={{gap: '2px'}}>
            <button className="border-2 border-gray-100 rounded-full p-2" onClick={handleButtonClick}>+</button>
            <div style={{display: isDisplayed ? 'block' : 'none'}}>
                <Overlay></Overlay>
                <div style={{zIndex: 1000, position: 'fixed'}}>
                    <button style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-full p-2" onClick={handleAddServer}>+</button>
                    <input style={{zIndex: 1000}} className="border-2 border-gray-100 rounded-md p-2" type="text" placeholder="server port" value={serverPort} onChange={(e) => setServerPort(e.target.value)} />
                </div>
            </div>
        </div>
    )
}

export default AddServerButton;