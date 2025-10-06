import { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { useServerState } from '../context/ServerContext';
import { useUsernameState } from '../context/UsernameContext';

let globalSocket = null;
let globalIsConnected = false;
let lastEmittedUsername = null;
const connectionListeners = new Set();

const updateConnectionState = (connected) => {
  globalIsConnected = connected;
  connectionListeners.forEach(listener => listener(connected));
};

const getSocket = (serverValue) => {
  if (!globalSocket || globalSocket.disconnected) {
    globalSocket = io(`http://localhost:${serverValue}`);
    
    globalSocket.on('connect', () => updateConnectionState(true));
    globalSocket.on('disconnect', () => {
      updateConnectionState(false);
      lastEmittedUsername = null;
    });
  }
  return globalSocket;
};

const emitUsername = (username) => {
  if (globalSocket && globalIsConnected && username && username !== 'Anonymous' && username !== lastEmittedUsername) {
    globalSocket.emit('username message', username);
    lastEmittedUsername = username;
  }
};

export const useSocket = () => {
  const { usernameValue } = useUsernameState();
  const { serverValue } = useServerState();
  const [isConnected, setIsConnected] = useState(globalIsConnected);

  useEffect(() => {
    const socket = getSocket(serverValue);
    
    connectionListeners.add(setIsConnected);
    
    return () => {
      connectionListeners.delete(setIsConnected);
    };
  }, [serverValue]);

  useEffect(() => {
    emitUsername(usernameValue);
  }, [usernameValue, globalIsConnected]);

  return { socket: globalSocket, isConnected };
};