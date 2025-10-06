import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; 
import './index.css';
import { AuthProvider } from './context/AuthContext.jsx';
import { UsernameProvider } from './context/UsernameContext.jsx';
import { ChannelProvider } from './context/ChannelContext.jsx';
import { ServerProvider, AllServersProvider } from './context/ServerContext.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <UsernameProvider>
    <ServerProvider>
    <AllServersProvider>
    <AuthProvider>
        <ChannelProvider>
          <App></App>
        </ChannelProvider>
    </AuthProvider>
    </AllServersProvider>
    </ServerProvider>
    </UsernameProvider>
  </React.StrictMode>
);