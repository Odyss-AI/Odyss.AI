// src/pages/LoginPage/LoginPage.js
import React from 'react';
import Login from '../../components/Login/Login';
import styles from './LoginPage.module.css';  // Import des spezifischen CSS Modules

function LoginPage() {
    return (
        <div className={styles.loginPage}>
            <Login />
        </div>
    );
}

export default LoginPage;
