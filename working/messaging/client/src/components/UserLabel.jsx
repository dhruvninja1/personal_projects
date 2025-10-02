import React from 'react';
import multiavatar from '@multiavatar/multiavatar'
// Also try named import
import { multiavatar as multiavatarNamed } from '@multiavatar/multiavatar'

// Debug: Let's see what we're actually importing
console.log('=== MULTIAVATAR DEBUG ===');
console.log('multiavatar import:', multiavatar);
console.log('multiavatar keys:', multiavatar ? Object.keys(multiavatar) : 'null/undefined');
console.log('multiavatar constructor:', multiavatar ? multiavatar.constructor : 'null/undefined');
console.log('========================');

function UserLabel({ username }){
    console.log('UserLabel rendering for:', username);
    console.log('multiavatar function:', multiavatar);
    console.log('typeof multiavatar:', typeof multiavatar);
    
    try {
        // Try different ways to call multiavatar
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
        
        console.log('Generated avatar for', username, ':', avatar);
        console.log('Avatar type:', typeof avatar);
        console.log('Avatar length:', avatar ? avatar.length : 'null/undefined');
        
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