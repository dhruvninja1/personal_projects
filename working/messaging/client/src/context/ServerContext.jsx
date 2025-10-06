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

export const AllServersContext = createContext();

export const useAllServersState = () => useContext(AllServersContext);

export const AllServersProvider = ({ children }) => {
    const [allServersValue, setAllServersValue] = useState([3000]);

    const updateAllServersValue = (newValue) => {
        setAllServersValue(newValue);
    };

    const addServer = (server) => {
        setAllServersValue([...allServersValue, server]);
    };

    const contextValue = {
        allServersValue,
        updateAllServersValue,
        addServer,
    };
    return(
        <AllServersContext.Provider value={contextValue}>
            {children}
        </AllServersContext.Provider>
    )
}

export default AllServersProvider;