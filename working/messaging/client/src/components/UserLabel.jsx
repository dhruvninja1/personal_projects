import React from 'react';
import multiavatar from '@multiavatar/multiavatar'
import { multiavatar as multiavatarNamed } from '@multiavatar/multiavatar'


function UserLabel({ username }){
    try {
        let avatar;
        if (typeof multiavatar === 'function') {
            avatar = multiavatar(username);
        } else if (multiavatar && typeof multiavatar.default === 'function') {
            avatar = multiavatar.default(username);
        } else if (multiavatar && multiavatar.multiavatar) {
            avatar = multiavatar.multiavatar(username);
        } else if (typeof multiavatarNamed === 'function') {
            avatar = multiavatarNamed(username);
        } else {
            console.error('multiavatar is not a function:', multiavatar);
            console.error('multiavatarNamed is not a function:', multiavatarNamed);
            throw new Error('multiavatar is not callable');
        }
        
        
        return(
            <div className='flex items-center gap-2'>
                <div 
                    className='w-8 h-8'
                    dangerouslySetInnerHTML={{ __html: avatar }}>
                </div>
                <h1>{username}</h1>
            </div>
        )
    } catch (error) {
        console.error('Error generating avatar for', username, ':', error);
        return(
            <div className='flex items-center gap-2'>
                <div className='w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center'>
                    <span className='text-xs'>{username.charAt(0).toUpperCase()}</span>
                </div>
                <h1>{username}</h1>
            </div>
        )
    }
}

export default UserLabel;