import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; 
import './index.css';
import { UsernameProvider } from './UsernameContext.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <UsernameProvider>
      <App></App>
    </UsernameProvider>
  </React.StrictMode>,
);
