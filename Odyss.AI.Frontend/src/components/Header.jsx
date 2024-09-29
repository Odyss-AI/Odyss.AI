import React from 'react';
import '../assets/styles/Header.css'; // Importiere die CSS-Datei
import myLogo from '../assets/images/00015-2159209463-removebg-preview.png'; // Importiere das Logo-Bild

const Header = () => {
    return (
        <div className="header-container">
            {/* Verwende das eigene Logo */}
            <img src={myLogo} alt="Logo" className="header-logo" />
            <h1 className="header-title">Odyss.AI</h1>
            <div className="header-text">
                Sail to solutions with our answer-delivering boat!
            </div>
        </div>
    );
};

export default Header;
