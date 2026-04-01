import React, { createContext, useState, useEffect, useContext } from 'react';
import { onAuthStateChanged, signOut as firebaseSignOut } from 'firebase/auth';
import { auth } from '../firebase';
import { useUsernameState } from '../context/UsernameContext';
import { useAllServersState } from './ServerContext';

export const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

async function createUserOnBackend(user){
  const response = await fetch('${import.meta.env.VITE_API_URL}/createUser', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({email: user.email, username: user.displayName}),
  });
}

export const AuthProvider = ({ children }) => {
  const { updateUsernameValue } = useUsernameState();
  const { setServers } = useAllServersState();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function getServers(user) {
    try {
      const response = await fetch('${import.meta.env.VITE_API_URL}/getUserServers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: user.email }),
      });
      const data = await response.json();
      // data.servers is now [{name: "", port: int}, ...]
      // Map to frontend format and set all at once
      const formattedServers = data.servers.map(server => ({
        serverPort: server.port,
        serverName: server.name
      }));
      setServers(formattedServers);
    } catch (error) {
      console.error('Error fetching servers:', error);
    }
  }
  
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
      if (user) {
        console.log(user);
        updateUsernameValue(user.displayName || user.email || 'Anonymous');
        createUserOnBackend(user);
        getServers(user);
      }
    });

    return () => unsubscribe();
  }, []);

  const signOut = async () => {
    try {
      await firebaseSignOut(auth);
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const value = {
    user,
    loading,
    signOut
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
