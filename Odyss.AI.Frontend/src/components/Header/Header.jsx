// src/components/Header/Header.jsx
import React from 'react';
import styles from './Header.module.css';
import userIcon from '../../assets/Images/boat.png'; // Beispiel für das Benutzer-Icon
import logo from '../../assets/Images/boat.png'; // Beispiel für das Logo

function Header() {
    return (
        <header className={styles.header}>
            <img src={logo} alt="Logo" className={styles.logo} /> {/* Logo auf der linken Seite */}
            <h1 className={styles.title}>Sail to solutions with our answer-delivering boat!</h1> {/* Titel in der Mitte */}
            <img src={userIcon} alt="User Icon" className={styles.userIcon} /> {/* Benutzer-Icon auf der rechten Seite */}
        </header>
    );
}

export default Header;
