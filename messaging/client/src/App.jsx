import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import UsernameForm from './components/UsernameForm'
import ChannelList from './components/ChannelList'
import UserList from './components/UserList'

function App(){
    return(
        <div>
            <div className='flex justify-left'>
            <UsernameForm></UsernameForm>
            <ChannelList></ChannelList>
            <MessageContainer></MessageContainer>
            <UserList></UserList>
            </div>
        </div>
    )
}

export default App;