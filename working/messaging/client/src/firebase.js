// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDRLoFDhnLhxSKiKoYNVWsXxqu8I3Z-uFk",
  authDomain: "monkeychat-37355.firebaseapp.com",
  projectId: "monkeychat-37355",
  storageBucket: "monkeychat-37355.firebasestorage.app",
  messagingSenderId: "72604866247",
  appId: "1:72604866247:web:21c48a1ab2781cc21e50e2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Google Auth Provider
export const provider = new GoogleAuthProvider();