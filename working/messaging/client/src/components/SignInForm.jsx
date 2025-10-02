import { auth, provider } from "../firebase";
import { signInWithPopup, signOut } from "firebase/auth";
import React, { useState } from "react";
import { useUsernameState } from "../context/UsernameContext";
import { useSocket } from "./socket";

function SignInForm() {
  const [user, setUser] = useState(null);
  const { updateUsernameValue } = useUsernameState();
  const { socket } = useSocket();
  const handleSignIn = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
    console.log(result.user);
    updateUsernameValue(result.user.displayName);
    socket.emit('username message', result.user.displayName);
  };

  return (
    <div>
    {!user ? (
      <>
      <div className="overlay" id="overlay" style={{ position: 'fixed', 
                                                           top: 0, 
                                                           left: 0, 
                                                           width: '100%', 
                                                           height: '100%', 
                                                           backgroundColor: 'rgba(0, 0, 0, 0.5)', 
                                                           zIndex: 999 }}>
            </div>
      <button onClick={handleSignIn} style={{ position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 1000,
        padding: '12px 24px',
        fontSize: '16px',
        backgroundColor: '#4285f4',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer' }}>Sign in with Google</button>
      </>
    ) : (
      null
    )}
    </div>
  );
}

export default SignInForm;