import os
import subprocess
import platform

from app.config import Config

def save_and_convert_file(file, namehash) -> str:
    
    os.makedirs(Config['UPLOAD_FOLDER'], exist_ok=True)

    filename = namehash
    file_path = os.path.join(Config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Prüfen, ob die Datei bereits eine PDF ist
    if file_path.lower().endswith('.pdf'):
        return file_path  # Datei ist bereits PDF, Rückgabe des Pfads

    # Temp-Ausgabepfad für die konvertierte PDF-Datei
    output_path = os.path.join(Config['UPLOAD_FOLDER'], os.path.splitext(filename)[0] + '.pdf')

    # Erkennen des Betriebssystems
    os_command = 'soffice' if platform.system() == 'Windows' else 'libreoffice'
    try:
        subprocess.run([
            os_command, '--headless', '--convert-to', 'pdf', file_path, '--outdir', output_folder
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None

    # Rückgabe des PDF-Pfads, wenn die Konvertierung erfolgreich war
    return output_path if os.path.exists(output_path) else None
