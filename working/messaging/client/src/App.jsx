import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import ChannelList from './components/ChannelList'
import UserList from './components/UserList'
import SignInForm from './components/SignInForm';
import AddServerButton from './components/AddServerButton';
import ServerButtonList from './components/ServerButtonList';

function App(){
    return(
        <div>
            <div className='flex justify-left'>
            <SignInForm></SignInForm>
            <AddServerButton></AddServerButton>
            <ServerButtonList></ServerButtonList>
            <ChannelList></ChannelList>
            <MessageContainer></MessageContainer>
            <UserList></UserList>
            </div>
        </div>
    )
}

export default App;