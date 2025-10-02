import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import UsernameForm from './components/UsernameForm'

function App(){
    return(
        <div>
            <UsernameForm></UsernameForm>
            <MessageContainer></MessageContainer>
        </div>
    )
}

export default App;