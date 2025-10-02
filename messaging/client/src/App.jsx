import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import UsernameForm from './components/UsernameForm'
import ChannelButton from './components/ChannelButton'

function App(){
    return(
        <div>
            
            <UsernameForm></UsernameForm>
            <MessageContainer></MessageContainer>
            <ChannelButton name='Channel 1'></ChannelButton>
        </div>
    )
}

export default App;