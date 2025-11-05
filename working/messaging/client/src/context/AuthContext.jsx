import React, { createContext, useState, useEffect, useContext } from 'react';
import { onAuthStateChanged, signOut as firebaseSignOut } from 'firebase/auth';
import { auth } from '../firebase';
import { useUsernameState } from '../context/UsernameContext';

export const AuthContext = createContext();


export const useAuth = () => useContext(AuthContext);

async function createUserOnBackend(user){
  const response = await fetch('https://localhost:3002/createUser', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({email: user.email, username: user.displayName}),
  });
}

export const AuthProvider = ({ children }) => {
  const { updateUsernameValue } = useUsernameState();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
      console.log(user);
      updateUsernameValue(user.displayName || user.email || 'Anonymous');
      createUserOnBackend(user);
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
