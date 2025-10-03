import { auth, provider } from "../firebase";
import { signInWithPopup } from "firebase/auth";
import React from "react";
import { useAuth } from "../context/AuthContext";
import iconImage from "../images/icon.png";

function SignInForm() {
  const { user, signOut } = useAuth();

  const handleSignIn = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      console.log(result.user);
      // Username will be automatically updated via AuthContext -> UsernameContext
    } catch (error) {
      console.error('Error signing in:', error);
    }
  };

  const handleSignOut = () => {
    signOut();
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
        <div style={{ position: 'fixed', bottom: '10px', left: '10px', zIndex: 1000 }}>
          <span className="flex items-center">
            <img src={iconImage} style={{ width: '40px', height: '40px', marginRight: '10px' }} alt="User icon"></img>
            <a href = "https://docs.google.com/document/d/14qthcysK_eHjf15sBIM0eqJcFroW6JJlvqlsofu_LA0/edit?usp=sharing" className="text-xs text-gray-500">TOS</a>
            </span>
          
          <span style={{ marginRight: '10px', color: 'black' }}>
            Welcome, {user.displayName || user.email}!
          </span>
          <button onClick={handleSignOut} style={{
            padding: '8px 16px',
            fontSize: '14px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}>
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}

export default SignInForm;