import React, { useState } from 'react';
import { useUsernameState } from '../UsernameContext';
import { useSocket } from './socket';

function UsernameForm() {
    const [inputValue, setInputValue] = useState('');
    const { updateUsernameValue } = useUsernameState();
    const { socket } = useSocket();

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputValue.trim()) {
            updateUsernameValue(inputValue);
            socket.emit('username message', inputValue);
            setInputValue('');
        }
        overlay.style.display = 'none';
        popup.style.display = 'none';
    };

    return (
        <div>
            <div className="overlay" id="overlay" style={{ position: 'fixed', 
                                                           top: 0, 
                                                           left: 0, 
                                                           width: '100%', 
                                                           height: '100%', 
                                                           backgroundColor: 'rgba(0, 0, 0, 0.5)', 
                                                           zIndex: 999 }}>
            </div>
            <div className="popup" id="popup" style={{ position: 'fixed', 
                                                       top: '50%', 
                                                       left: '50%', 
                                                       transform: 'translate(-50%, -50%)', 
                                                       backgroundColor: 'white', 
                                                       borderRadius: '8px', 
                                                       boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', 
                                                       zIndex: 1000, 
                                                       padding: '20px', 
                                                       display: 'flex', 
                                                       flexDirection: 'column', 
                                                       alignItems: 'center', 
                                                       gap: '10px' }}>
                <form onSubmit={handleSubmit}>
                    <input 
                        type="text" 
                        placeholder="Enter your username"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                    />
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default UsernameForm;
