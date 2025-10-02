import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; 
import './index.css';
import { AuthProvider } from './context/AuthContext.jsx';
import { UsernameProvider } from './context/UsernameContext.jsx';
import { ChannelProvider } from './context/ChannelContext.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <UsernameProvider>
        <ChannelProvider>
          <App></App>
        </ChannelProvider>
      </UsernameProvider>
    </AuthProvider>
  </React.StrictMode>,
);
