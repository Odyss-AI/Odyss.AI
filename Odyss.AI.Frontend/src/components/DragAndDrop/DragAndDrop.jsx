// src/components/DragAndDrop/DragAndDrop.jsx
import {useState} from "react";
import React from 'react';
import styles from './DragAndDrop.module.css';
import useFileStore from "../../store/fileStore.jsx";

function DragAndDrop() {
    const [dragActive, setDragActive] = React.useState(false);
    const uploadFile = useFileStore((state) =>state.uploadFile);

    return (
        <div className={styles.dragAndDrop}>
            {/* Inhalt der DragAndDrop-Komponente hier */}
            <p>Drag and drop your files here</p>
        </div>
    );
}

export default DragAndDrop;
