import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import ChannelList from './components/ChannelList'
import UserList from './components/UserList'
import SignInForm from './components/SignInForm';

function App(){
    return(
        <div>
            <div className='flex justify-left'>
            <SignInForm></SignInForm>
            <ChannelList></ChannelList>
            <MessageContainer></MessageContainer>
            <UserList></UserList>
            </div>
        </div>
    )
}

export default App;