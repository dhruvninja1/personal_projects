import React, { createContext, useState, useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';

export const UsernameContext = createContext();

export const useUsernameState = () => useContext(UsernameContext);

export const UsernameProvider = ({ children }) => {
    const [usernameValue, setUsernameValue] = useState('');
    const { user } = useAuth();
  
    // Update username when user authentication state changes
    useEffect(() => {
      if (user) {
        setUsernameValue(user.displayName || user.email || 'Anonymous');
      } else {
        setUsernameValue('');
      }
    }, [user]);
  
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