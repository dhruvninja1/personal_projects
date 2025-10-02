import React, { useState } from 'react';


function Message( {key, sender, content, color, timestamp} ){
    return(
        <div className='w-1/2'>
            <div className={`flex flex-col max-w-lg rounded-xl shadow-md bg-gray-200 text-gray-800`}>
                <div className="px-3 pt-2 text-xs font-semibold" style={{ color: color }}>
                    {sender}
                </div>
                
                <div className={`px-3 pt-1 pb-1 text-lg bg-gray-200 text-gray-800`}>
                    {content}
                </div>
                <div className="px-3 pb-2 text-[10px] opacity-75 self-end">
                    {timestamp}
                </div>
            </div>
        </div>
    )
}

export default Message;
