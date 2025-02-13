import os
import subprocess
import asyncio
import logging

from app.config import config

async def save_and_convert_file(file, hash_filename: str, db) -> str:
    
    file_path_original = os.path.join(config.local_doc_path, hash_filename)

    try:
        await file.save(file_path_original)
    except Exception as e:
        print(f"Error while saving file: {str(e)}")
        logging.error(f"Error while saving file: {str(e)}")
        return None
    
    file_extension = file_path_original.rsplit('.', 1)[1].lower()
    base_filename = os.path.splitext(os.path.basename(file_path_original))[0]

    if file_extension == 'pdf':
        converted_file = await asyncio.to_thread(open, file_path_original, 'rb')
        return file_path_original, converted_file
        
    elif file_extension in ('docx', 'pptx'):
        # Zielpfad für konvertierte Datei
        output_path = os.path.join(config.local_doc_path, f"{base_filename}.pdf")

        try:
            # Konvertierung mit LibreOffice (soffice) in PDF
            process = await asyncio.create_subprocess_exec(
                'soffice', '--headless', '--convert-to', 'pdf', '--outdir', config.local_doc_path, file_path_original,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            # Überprüfen, ob Konvertierung erfolgreich war
            if process.returncode != 0:
                print(f"LibreOffice Konvertierungsfehler: {stderr.decode()}")
                return None
            
            # Originaldatei entfernen, da Konvertierung abgeschlossen
            await asyncio.to_thread(os.remove, file_path_original)

            # Nun die konvertierte PDF-Datei hochladen
            converted_file = await asyncio.to_thread(open, output_path, 'rb')
            return output_path, converted_file
        except Exception as e:
            print(f"Fehler bei der Konvertierung von {file_path_original}: {e}")
            logging.error(f"Fehler bei der Konvertierung von {file_path_original}: {e}")
            return None

    return None