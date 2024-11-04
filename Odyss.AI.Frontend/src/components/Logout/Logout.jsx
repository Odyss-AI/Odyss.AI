// src/components/Logout.js
import React from 'react';
import useAuthStore from '../../store/authStore.jsx';

function Logout() {
    const logout = useAuthStore((state) => state.logout);  // Logout-Funktion holen

    const handleLogout = () => {
        logout();  // Logout-Logik hier
    };

    return (
        <div className="logout">
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default Logout;