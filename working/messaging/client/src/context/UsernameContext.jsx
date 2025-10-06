import React, { createContext, useState, useContext } from 'react';

export const UsernameContext = createContext();

export const useUsernameState = () => useContext(UsernameContext);

export const UsernameProvider = ({ children }) => {
    const [usernameValue, setUsernameValue] = useState('Anonymous');
  
    const updateUsernameValue = (newValue) => {
      setUsernameValue(newValue);
    };
  
    const contextValue = {
      usernameValue,
      updateUsernameValue,
    };
  
    return (
      <UsernameContext.Provider value={contextValue}>
        {children}
      </UsernameContext.Provider>
    );
  };
