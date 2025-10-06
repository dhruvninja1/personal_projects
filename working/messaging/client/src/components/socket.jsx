import { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { useServerState } from '../context/ServerContext';
import { useUsernameState } from '../context/UsernameContext';

let globalSocket = null;
let globalIsConnected = false;
let lastEmittedUsername = null;
let currentServerPort = null;
const connectionListeners = new Set();

const updateConnectionState = (connected) => {
  globalIsConnected = connected;
  connectionListeners.forEach(listener => listener(connected));
};

const getSocket = (serverValue) => {
  // If server port changed, disconnect old socket and create new one
  if (currentServerPort !== serverValue) {
    if (globalSocket) {
      globalSocket.disconnect();
      globalSocket = null;
    }
    currentServerPort = serverValue;
  }
  
  if (!globalSocket || globalSocket.disconnected) {
    globalSocket = io(`http://localhost:${serverValue}`);
    
    globalSocket.on('connect', () => {
      console.log(`Connected to server on port ${serverValue}`);
      updateConnectionState(true);
      // Emit username immediately after connection
      if (lastEmittedUsername) {
        globalSocket.emit('username message', lastEmittedUsername);
        console.log(`Re-emitted username: ${lastEmittedUsername}`);
      }
    });
    globalSocket.on('disconnect', () => {
      console.log(`Disconnected from server on port ${serverValue}`);
      updateConnectionState(false);
      // Don't reset lastEmittedUsername here - we need it for reconnection
    });
  }
  return globalSocket;
};

const emitUsername = (username, forceEmit = false) => {
  if (globalSocket && globalIsConnected && username && username !== 'Anonymous' && (forceEmit || username !== lastEmittedUsername)) {
    globalSocket.emit('username message', username);
    lastEmittedUsername = username;
    console.log(`Emitted username: ${username}`);
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

  // Force emit username when server changes and we're connected
  useEffect(() => {
    if (globalIsConnected && usernameValue && usernameValue !== 'Anonymous') {
      emitUsername(usernameValue, true);
    }
  }, [serverValue, globalIsConnected]);

  return { socket: globalSocket, isConnected };
};