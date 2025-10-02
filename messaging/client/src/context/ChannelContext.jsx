import React, { createContext, useState, useContext } from 'react';

export const ChannelContext = createContext();

export const useChannelState = () => useContext(ChannelContext);

export const ChannelProvider = ({ children }) => {
    const [channelValue, setChannelValue] = useState('Initial Channel Data');
  
    const updateChannelValue = (newValue) => {
      setChannelValue(newValue);
    };
  
    const contextValue = {
      channelValue,
      updateChannelValue,
    };
  
    return (
      <ChannelContext.Provider value={contextValue}>
        {children}
      </ChannelContext.Provider>
    );
  };