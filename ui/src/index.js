import React from 'react';
import ReactDOM from 'react-dom'; // For react 17
// For react 18: import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

import { FronteggProvider } from '@frontegg/react';

const contextOptions = {}
const authOptions = {
 // keepSessionAlive: true // Uncomment this in order to maintain the session alive
};


/**
 * Render the application.
 */
function render(){
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
        <FronteggProvider contextOptions={contextOptions}
        hostedLoginBox={true}
        authOptions={authOptions}>
            <App />
        </FronteggProvider>,
        document.getElementById('root')
    );
}

// Resolve the API's base URL.
const apiBaseUrl =
    process.env.REACT_APP__API__BASE_URL ||
    `${window.location.protocol}://${window.location.host}`;


// If the environment includes Frontegg configuration, let's use it!
if (process.env.REACT_APP__FRONTEGG__BASE_URL)
{
    contextOptions.baseUrl = process.env.REACT_APP__FRONTEGG__BASE_URL;
    contextOptions.clientId = process.env.REACT_APP__FRONTEGG__CLIENT_ID;
    render();
} else {  // Otherwise, try to get it from the local API source.
    const configUrl = `${apiBaseUrl}/api/config/ui`;
    fetch(configUrl)
        .then((response) => response.json())
        .then((data) => {
            contextOptions.baseUrl = data.auth.frontegg.baseUrl;
            contextOptions.clientId = data.auth.frontegg.clientId;
        })
        .then(() => render())
}
