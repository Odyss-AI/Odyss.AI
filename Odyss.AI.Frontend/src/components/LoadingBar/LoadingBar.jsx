import React from 'react';
import styles from './LoadingBar.module.css';

export default function LoadingBar({progress}) {
    return (
        <div className={styles.loadingBarContainer}>
            <div className={styles.loadingBar} style={{width: `${progress}%`}}></div>
        </div>
    )
}