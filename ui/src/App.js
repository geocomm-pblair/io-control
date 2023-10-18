import './App.css';
import React, { useState } from 'react';
import Select from 'react-select';
import {
  useAuth,
  useAuthActions,
  useLoginWithRedirect,
  ContextHolder,
} from "@frontegg/react";
import { AdminPortal } from '@frontegg/react'

function App() {
  const { switchTenant } = useAuthActions();
  const { user, isAuthenticated } = useAuth();
  const loginWithRedirect = useLoginWithRedirect();

  const showSettings = () => {
    AdminPortal.show();
  };

  const logout = () => {
    const baseUrl = ContextHolder.getContext().baseUrl;
    window.location.href = `${baseUrl}/oauth/logout?post_logout_redirect_uri=${window.location}`;
  };

  const [selectedTenant, setSelectedTenant] = useState(null);

  const handleSwitchTenant = () => {
    if (selectedTenant) {
      switchTenant({ tenantId: selectedTenant });
    } else {
      console.log("No tenant selected.");
    }
  };

  const tenantOptions = user?.tenantIds?.map(tenantId => ({
    value: tenantId,
    label: tenantId,
  })) || [];

  const activeTenantOption = tenantOptions.find(option => option.value === selectedTenant);

  return (
    <div className="App">
      { isAuthenticated ? (
        <div>
          <div>
            <img src={user?.profilePictureUrl} alt={user?.name}/>
          </div>
          <div>
            <span>Logged in as: {user?.name}</span>
          </div>
          <div>
            <button onClick={() => alert(user.accessToken)}>What is my access token?</button>
            <div>
              <span>Select tenant</span>
              <Select
                options={tenantOptions}
                value={activeTenantOption} // Highlight the active tenant
                onChange={(selectedOption) => setSelectedTenant(selectedOption.value)}
              />
            </div>
            <button onClick={handleSwitchTenant}>Select Active Tenant</button>
          </div>
          <div>
            <button onClick={() => logout()}>Click to logout</button>
            <button onClick={showSettings}>Settings</button>
          </div>
        </div>
      ) : (
        <div>
          <button onClick={() => loginWithRedirect()}>Click me to login</button>
        </div>
      )}
    </div>
  );
}

export default App;
