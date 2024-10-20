import os
import subprocess
import sys

def setup_virtualenv():
    # Überprüfen, ob der Ordner 'venv' existiert
    if not os.path.exists('venv'):
        print("Erstelle virtuelle Umgebung...")
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])
    else:
        print("Virtuelle Umgebung existiert bereits.")

    # Aktivieren der virtuellen Umgebung und Installieren der Pakete
    if os.name == 'nt':  # Windows
        activate_script = os.path.join('venv', 'Scripts', 'activate')
    else:  # Unix oder MacOS
        activate_script = os.path.join('venv', 'bin', 'activate')

    print("Aktiviere virtuelle Umgebung und installiere Pakete...")
    subprocess.check_call(f"{activate_script} && pip install -r requirements.txt", shell=True)

if __name__ == "__main__":
    setup_virtualenv()