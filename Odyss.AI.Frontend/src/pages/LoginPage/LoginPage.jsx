import React, { useState } from 'react';
import Login from '../../components/Login/Login';
import styles from './LoginPage.module.css';  // Import des spezifischen CSS Modules
import videoBg from '../../assets/Videos/background1.mp4';  // Beispielhafter Import des Videos
import Header from '../../components/Header/Header'; // Import des Headers
import { createUser } from '../../utils';  // Import der Funktion createUser aus dem userService

function LoginPage() {
    const [isRegister, setIsRegister] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const toggleRegister = () => {
        setIsRegister((prev) => !prev);
    };

    const handleRegister = async () => {
        console.log('Register');
        if (username && password && confirmPassword) {
            if (password !== confirmPassword) {
                alert('Passwords do not match');
                return;
            }
            const user = await createUser(username, password);
            if (user.error) {
                console.log(user.error);
                alert(user.error);
                return;
            }
            login(user);  // Login-Logik hier
        } else {
            alert('Please enter username and password');
        }
    };

    return (
        <div className={styles.loginPage}>
            {/* <video autoPlay loop muted className={styles.videoBackground}>
                <source src={videoBg} type="video/mp4" />
                Your browser does not support the video tag.
            </video> */}
            <div className={styles.loginFormContainer}>
                {isRegister ? (
                    <div className={styles.registerForm}>
                        <h2>Registrieren</h2>
                        <input
                            type="text"
                            placeholder="Username"
                            className={styles.inputField}
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            className={styles.inputField}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Confirm Password"
                            className={styles.inputField}
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                        <button onClick={handleRegister} className={styles.submitButton}>Register</button>
                        <p className={styles.toggleText} onClick={toggleRegister}>
                            Bereits registriert? Zum Login wechseln
                        </p>
                    </div>
                ) : (
                    <div>
                        <Login />
                        <p className={styles.toggleText} onClick={toggleRegister}>
                            Noch keinen Account? Jetzt registrieren
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default LoginPage;