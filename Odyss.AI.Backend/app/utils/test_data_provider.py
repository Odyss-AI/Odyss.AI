from app.models.user import User, Document, TextChunk, Image
from bson.objectid import ObjectId

def get_test_user():
    return User(
        id="5f2b6b3b4f3d453e2f6e1c7c",
        username="testuser",
        documents=[]
    )

def get_test_document(path: str):
    return Document(
        id=str(ObjectId()),
        doc_id=path,
        name="testdocument",
        timestamp="2020-08-05T12:00:00",
        doclink="",
        summary="This is a test document",
        imgList=[],
        textList = [
            TextChunk(
                id=str(ObjectId()), 
                text="Künstliche Intelligenz (KI) ist ein Bereich der Informatik, der sich mit der Entwicklung von Systemen befasst, die Aufgaben ausführen können, die normalerweise menschliche Intelligenz erfordern. Dazu gehören das Erkennen von Mustern, das Lernen aus Daten und das Treffen von Entscheidungen. KI wird in vielen Bereichen wie Medizin, Automobilindustrie und Finanzen eingesetzt.", 
                page=1,
                formula=["f(x) = sin(x) + cos(x)"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Machine Learning (ML) ist ein Teilbereich der KI, der es Maschinen ermöglicht, ohne explizite Programmierung aus Daten zu lernen. ML-Modelle werden auf Basis von Trainingsdaten optimiert, um Muster zu erkennen und Vorhersagen zu treffen. Bekannte ML-Methoden umfassen überwachtes, unüberwachtes und verstärkendes Lernen.", 
                page=2,
                formula=["f'(x) = 2x"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Neuronale Netzwerke sind eine Schlüsseltechnologie im Bereich des maschinellen Lernens. Inspiriert vom menschlichen Gehirn bestehen sie aus Schichten von Neuronen, die miteinander verbunden sind. Durch Anpassung der Gewichtungen dieser Verbindungen lernen die Netzwerke, Muster in Daten zu erkennen und komplexe Probleme zu lösen.", 
                page=3,
                formula=["f(x) = e^x"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Deep Learning ist eine Methode des maschinellen Lernens, die auf tiefen neuronalen Netzwerken basiert. Es handelt sich um eine Technik, die in der Lage ist, große Mengen an unstrukturierten Daten wie Bilder, Videos oder Texte zu verarbeiten. Deep Learning hat große Fortschritte in Bereichen wie Spracherkennung und Bildverarbeitung ermöglicht.", 
                page=4,
                formula=["f(x) = log(x)"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Quantencomputing ist ein aufstrebendes Gebiet der Informatik, das Quantenmechanik nutzt, um Rechenoperationen durchzuführen. Im Gegensatz zu klassischen Computern, die mit Bits arbeiten, verwenden Quantencomputer Qubits, die in mehreren Zuständen gleichzeitig existieren können. Dies könnte die Lösung komplexer Probleme, wie etwa in der Kryptographie, revolutionieren.", 
                page=5,
                formula=["f(x, y) = x^2 + y^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Blockchain ist eine Technologie, die es ermöglicht, Daten sicher und dezentral zu speichern. Ursprünglich als Grundlage für Kryptowährungen wie Bitcoin entwickelt, findet sie mittlerweile Anwendung in verschiedenen Bereichen wie Lieferketten, Wahlen und digitalen Identitäten. Die Daten werden in Blöcken gespeichert, die durch kryptographische Verfahren miteinander verknüpft sind.", 
                page=6,
                formula=["f(x) = a^x"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Das Internet der Dinge (IoT) bezieht sich auf ein Netzwerk von physischen Objekten, die über das Internet miteinander verbunden sind und Daten austauschen. Von Haushaltsgeräten bis hin zu industriellen Maschinen ermöglicht IoT die Automatisierung und Fernsteuerung von Prozessen. Dies hat weitreichende Auswirkungen auf verschiedene Industrien, einschließlich der Fertigung und des Gesundheitswesens.", 
                page=7,
                formula=["f(x) = 1/x"]),

            TextChunk(
                id=str(ObjectId()), 
                text="5G ist die fünfte Generation der Mobilfunktechnologie, die schnellere Internetverbindungen und geringere Latenzzeiten als ihre Vorgänger bietet. Diese Technologie ermöglicht neue Anwendungen wie autonomes Fahren, Augmented Reality und das Internet der Dinge. 5G wird als Schlüsseltechnologie für die digitale Transformation vieler Industrien angesehen.", 
                page=8,
                formula=["f(x) = x^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Augmented Reality (AR) ist eine Technologie, die digitale Inhalte in die reale Welt einbettet. Mit Hilfe von Kameras und Bildschirmen können Benutzer interaktive virtuelle Objekte sehen und manipulieren, während sie ihre Umgebung betrachten. AR findet Anwendung in Bereichen wie Bildung, Gaming und Medizin.", 
                page=9,
                formula=["f(x) = tan(x)"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Virtual Reality (VR) erzeugt eine vollständig künstliche Umgebung, die den Benutzer durch visuelle, auditive und manchmal haptische Reize in eine simulierte Welt eintauchen lässt. VR wird in der Unterhaltung, im Training von Fachkräften und in der Therapie eingesetzt, um immersive Erfahrungen zu bieten.", 
                page=10,
                formula=["f(x) = 1 - x^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Cloud Computing ermöglicht es Benutzern, Rechenressourcen wie Speicher, Rechenleistung und Anwendungen über das Internet zu nutzen, anstatt diese lokal auf ihren Geräten zu betreiben. Dienste wie Amazon Web Services, Google Cloud und Microsoft Azure bieten skalierbare Lösungen für Unternehmen und Einzelpersonen.", 
                page=11,
                formula=["f(x) = x!"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Cybersecurity ist der Bereich der Informatik, der sich mit dem Schutz von Netzwerken, Computern und Daten vor unbefugtem Zugriff und Cyberangriffen beschäftigt. Sicherheitsmaßnahmen umfassen Firewalls, Verschlüsselung und die Verwendung von sicheren Passwörtern. Angriffe wie Phishing und Ransomware stellen ernsthafte Bedrohungen für die digitale Sicherheit dar.", 
                page=12,
                formula=["f(x) = x mod 2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Big Data bezieht sich auf extrem große und komplexe Datensätze, die mit traditionellen Methoden der Datenverarbeitung nicht effektiv analysiert werden können. Mit der Zunahme von Datenquellen wie sozialen Medien, Sensoren und mobilen Geräten wächst der Bedarf an neuen Technologien und Ansätzen zur Analyse und Verwaltung dieser Daten.", 
                page=13,
                formula=["f(x) = x^n"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Kryptographie ist die Wissenschaft der Verschlüsselung von Informationen, um sie vor unbefugtem Zugriff zu schützen. Moderne kryptographische Verfahren basieren auf mathematischen Algorithmen, die sicherstellen, dass nur autorisierte Parteien Zugang zu den Daten erhalten. Sie spielen eine zentrale Rolle in der Informationssicherheit und bei der Übertragung sensibler Daten über das Internet.", 
                page=14,
                formula=["f(x) = x + y"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Autonomes Fahren bezieht sich auf Fahrzeuge, die mithilfe von Sensoren, Kameras und Algorithmen in der Lage sind, ohne menschliches Eingreifen zu navigieren. Diese Technologie verspricht, den Verkehr sicherer und effizienter zu machen. Zu den Herausforderungen gehören jedoch rechtliche und ethische Fragen sowie die Integration in bestehende Infrastrukturen.", 
                page=15,
                formula=["f(x) = v*t"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Das menschliche Gehirn ist ein hochkomplexes Organ, das als Steuerzentrale des Körpers fungiert. Es besteht aus Milliarden von Neuronen, die durch Synapsen miteinander verbunden sind und elektrische Signale austauschen. Das Gehirn ist für unsere Wahrnehmungen, Gedanken und Handlungen verantwortlich.", 
                page=16,
                formula=["f(x) = x/2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Genetik ist die Wissenschaft, die sich mit der Vererbung von Eigenschaften bei Organismen befasst. Sie untersucht die Struktur und Funktion von Genen und wie diese an Nachkommen weitergegeben werden. Fortschritte in der Genetik haben zu wichtigen Entwicklungen in der Medizin geführt, wie etwa der Gentechnik und der personalisierten Medizin.", 
                page=17,
                formula=["f(x) = x^2 + y^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Die Relativitätstheorie, entwickelt von Albert Einstein, beschreibt die Wechselwirkung von Raum, Zeit und Gravitation. Die spezielle Relativitätstheorie befasst sich mit der Bewegung bei konstanten Geschwindigkeiten, während die allgemeine Relativitätstheorie die Gravitation als Krümmung der Raumzeit erklärt. Diese Theorien haben unser Verständnis des Universums revolutioniert.", 
                page=18,
                formula=["E = mc^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Künstliche Organe sind mechanische oder biologische Vorrichtungen, die entwickelt wurden, um die Funktion natürlicher Organe zu ersetzen. Sie werden verwendet, um Patienten mit Organversagen zu behandeln und bieten eine lebenswichtige Alternative zur Organtransplantation. Zu den bekannten künstlichen Organen gehören Herzschrittmacher, künstliche Nieren und Herz-Lungen-Maschinen.", 
                page=19,
                formula=["f(x) = dV/dt"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Erneuerbare Energien stammen aus Quellen, die sich ständig erneuern oder unerschöpflich sind, wie Sonne, Wind und Wasser. Der Übergang zu erneuerbaren Energien ist ein wesentlicher Bestandteil der Bemühungen, den Klimawandel zu bekämpfen und die Abhängigkeit von fossilen Brennstoffen zu reduzieren. Sie bieten eine nachhaltige und saubere Alternative zur Energieversorgung.", 
                page=20,
                formula=["P = E/t"]),
            
            TextChunk(
                id=str(ObjectId()), 
                text="Die Fotosynthese ist der Prozess, durch den Pflanzen, Algen und einige Bakterien Lichtenergie in chemische Energie umwandeln. Dabei wird Kohlendioxid und Wasser in Glukose und Sauerstoff umgewandelt. Fotosynthese ist der grundlegende Prozess, der das Leben auf der Erde unterstützt, da sie die primäre Energiequelle für fast alle Lebewesen ist.", 
                page=21,
                formula=["6CO2 + 6H2O -> C6H12O6 + 6O2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Nanotechnologie beschäftigt sich mit der Manipulation von Materie auf atomarer und molekularer Ebene. Sie hat das Potenzial, in vielen Bereichen wie Medizin, Elektronik und Materialwissenschaften bahnbrechende Innovationen zu ermöglichen. Anwendungen umfassen Nanomedizin, bei der winzige Teilchen zur gezielten Behandlung von Krankheiten eingesetzt werden.", 
                page=22,
                formula=["f(x) = 10^-9"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Klimawandel bezieht sich auf langfristige Veränderungen des Wettermusters auf der Erde, insbesondere durch die Erhöhung der globalen Durchschnittstemperaturen. Diese Veränderungen sind weitgehend auf menschliche Aktivitäten zurückzuführen, insbesondere auf die Verbrennung fossiler Brennstoffe. Der Klimawandel hat weitreichende Auswirkungen auf Ökosysteme, Wirtschaft und Gesellschaft.", 
                page=23,
                formula=["f(CO2) = T + ΔT"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Schwarze Löcher sind Regionen im Weltraum, in denen die Gravitationskraft so stark ist, dass nichts, nicht einmal Licht, entkommen kann. Sie entstehen, wenn massereiche Sterne am Ende ihres Lebens kollabieren. Schwarze Löcher spielen eine wichtige Rolle in der Astrophysik und können durch ihre Auswirkungen auf umliegende Materie und Licht nachgewiesen werden.", 
                page=24,
                formula=["R_s = 2GM/c^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Das Sonnensystem besteht aus der Sonne und den Himmelskörpern, die sie umkreisen, darunter acht Planeten, Monde, Asteroiden und Kometen. Die Erde ist der dritte Planet von der Sonne und der einzige bekannte Ort im Universum, der Leben beherbergt. Die Entstehung und Struktur des Sonnensystems sind Gegenstand intensiver wissenschaftlicher Forschung.", 
                page=25,
                formula=["F = G * (m1*m2)/r^2"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Die Evolutionstheorie, aufgestellt von Charles Darwin, beschreibt, wie Arten durch natürliche Selektion über Generationen hinweg Veränderungen erfahren. Individuen mit Eigenschaften, die besser an ihre Umwelt angepasst sind, haben eine höhere Überlebens- und Fortpflanzungsrate. Dies führt zu einer allmählichen Veränderung der genetischen Merkmale einer Population.", 
                page=26,
                formula=["ΔG = ΔH - TΔS"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Das menschliche Immunsystem ist ein komplexes Netzwerk von Zellen, Geweben und Organen, das den Körper vor Infektionen und Krankheiten schützt. Es erkennt und bekämpft Eindringlinge wie Bakterien, Viren und Parasiten. Eine starke Immunabwehr ist entscheidend für die Gesundheit und das Überleben.", 
                page=27,
                formula=["f(x) = 1 / (1 + e^-x)"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Die Digitalisierung beschreibt den Prozess, bei dem analoge Informationen in digitale Formate umgewandelt werden. Sie hat viele Bereiche der Gesellschaft verändert, von der Arbeitswelt bis hin zur Freizeit. Die fortschreitende Digitalisierung hat neue Geschäftsmodelle hervorgebracht und die Art und Weise, wie wir kommunizieren und Informationen konsumieren, grundlegend verändert.", 
                page=28,
                formula=["f(digital) = 0 oder 1"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Roboter sind mechanische Geräte, die dazu entwickelt wurden, Aufgaben automatisch oder halbautomatisch auszuführen. Sie werden in einer Vielzahl von Bereichen eingesetzt, von der industriellen Fertigung über die Medizin bis hin zur Weltraumforschung. Fortschritte in der Robotik haben die Fähigkeiten dieser Maschinen stark erweitert, sodass sie heute komplexe und präzise Aufgaben erledigen können.", 
                page=29,
                formula=["f(x) = ma"]),

            TextChunk(
                id=str(ObjectId()), 
                text="Die Biodiversität bezieht sich auf die Vielfalt des Lebens auf der Erde, einschließlich der genetischen Vielfalt innerhalb von Arten, der Artenvielfalt in Ökosystemen und der Vielfalt der Ökosysteme selbst. Sie ist von entscheidender Bedeutung für das Funktionieren der Ökosysteme und das Überleben des Menschen, da sie Nahrung, sauberes Wasser und andere Ressourcen liefert.", 
                page=30,
                formula=["f(x) = Σ species"]),
        ]

        )