import React, { useState } from 'react';
import MessageContainer from './components/MessageContainer'
import ChannelList from './components/ChannelList'
import UserList from './components/UserList'
import SignInForm from './components/SignInForm';
import ServerButtonList from './components/ServerButtonList';
import Pause from './components/Pause';

function App(){
    return(
        <div>
            <div className='flex justify-left'>
                <SignInForm></SignInForm>
                <Pause></Pause>
                <ServerButtonList></ServerButtonList>
                <ChannelList></ChannelList>
                <MessageContainer></MessageContainer>
                <UserList></UserList>
            </div>
        </div>
    )
}

export default App;