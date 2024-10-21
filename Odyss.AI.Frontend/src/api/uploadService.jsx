// src/api/uploadService.js
export const uploadPDFs = async (files) => {
    const formData = new FormData();

    files.forEach((file) => {
        formData.append('files', file);
    });

    try {
        const response = await fetch('https://your-backend-url.com/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Fehler beim Hochladen der Dateien');
        }

        return await response.json();
    } catch (error) {
        console.error('Upload-Fehler:', error);
        throw error;
    }
};
