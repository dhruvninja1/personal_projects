import React, { createContext, useState, useContext } from 'react';

export const ServerContext = createContext();

export const useServerState = () => useContext(ServerContext);

export const ServerProvider = ({ children }) => {
    const [serverValue, setServerValue] = useState(3000);
  
    const updateServerValue = (newValue) => {
      setServerValue(newValue);
    };
  
    const contextValue = {
      serverValue,
      updateServerValue,
    };
  
    return (
      <ServerContext.Provider value={contextValue}>
        {children}
      </ServerContext.Provider>
    );
  };