#SNSK,PLRS

"""
Aufgabe 1
Funktion: Aufgabenverwaltung
add_task -> legt eine Aufgabe an (Name, Fälligkeit, Priorität, ID)
remove_task -> löscht eine Aufgabe per ID
mark_done -> markiert eine Aufgabe per Namen als erledigt
show_tasks -> gibt alle Aufgaben in der Konsole aus
process_tasks -> ändert den Status einer zufälligen Aufgabe
calculate_task_average -> berechnet den Durchschnitt der IDs (Sinn?)
upcoming_tasks -> gibt Aufgaben sortiert nach Name aus

Verständnisprobleme:
- ein Task ist eine Liste von teilweise magischen Werten
    - task[0]-[5]
    - Bedeutung von task[4] oder task[5] ist nicht erkennbar
- Unbegründete Kommentare wie "Wichtig! Nicht verändern!"
- Funktionsnamen sagen nicht immer etwas über die Funktion aus -> process_tasks, cleanup, calculate_task_average etc.
- Ergebnis der Ausgabe der Aufgaben ist zufällig und nicht eindeutig vorhersehbar
- Variablen werden befüllt, aber nicht benutzt, z.B. backup_tasks, user1

Aufgabe 2
Positiv:
- kleine, kurze Funktionen
- überwiegend sprechende Variablennamen (due_date, priority)
- remove_task meldet Erfolg/Misserfolg über Rückgabewert
- Formatierung überwiegend gut
- Standardwerte für optionale Parameter (priority, task_id)
- nutzt Standardbibliotheken (datetime, random)

Negativ:
1. Struktur
- globale Variablen statt Klasse
- tasks -> None statt {}
- task ist Liste mit Indizes statt dataclass/dict
2. Lesbarkeit / Doku
- keine Docstrings, keine Type Hints
- unbegründete Kommentare "Wichtig! Nicht verändern!"
- TODO nach return ohne Erklärung, was fehlt
- magische Werte (Prio 3, random.randint, user1)
- unnötiges global
- ungenutzte Schleifenvariable task_id in mark_done
3. Robustheit / Fehler
- Datum wird als String verglichen
- zufällige ID-Vergabe kann zu Fehlern bzw. Überschreiben führen (Kollision)
- gemischte ID-Typen möglich
- upcoming_tasks sortiert nach Name und nicht nach Datum, es werden auch erledigte Aufgaben geliefert (Ausgabe ist: "Offene Aufgaben")
- mark_done -> gibt immer "Erledigt" zurück, auch wenn keine Aufgabe gefunden wurde
- process_tasks -> zufälliges Umschalten des Status macht keinen Sinn
- backup_tasks -> speichert Referenzen auf dieselben Listen, kein echtes Backup
- backup_tasks -> wird bei remove_task nicht aktualisiert
- cleanup -> löscht Aufgaben ohne Rückmeldung
- keine Validierung der Eingaben
4. Wartbarkeit
- get_task_count sehr kompliziert
- Vergleich == None statt is None
- Ausgabeformat (print) fest in der Logik

Verbesserungen:
- Task als @dataclass mit Feldern name, due_date etc.
- TaskManager-Klasse statt globaler Variablen
- fortlaufende IDs statt Zufall
- upcoming_tasks -> nur offene Aufgaben nach Fälligkeit
- sprechende Namen verwenden
- Konstanten für Standardwerte verwenden
- Eingabevalidierung
- sinnvolle Kommentare

"""
import datetime
import random

tasks = None
backup_tasks = {}


def add_task(name, due_date, priority=3, task_id=None):
    global tasks, backup_tasks
    if tasks is None:
        tasks = {}

    if task_id == None:
        task_id = len(tasks) + random.randint(2, 7)  # Wichtig! Nicht verändern!
    task = [name, due_date, priority, False, "user1",
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M")]
    tasks[task_id] = task
    backup_tasks[task_id] = task
    return task_id


def remove_task(task_id):
    global tasks
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


def mark_done(task_name):
    global tasks
    for task_id, task in tasks.items():
        if task[0] == task_name:
            task[3] = True
    return "Erledigt"


def show_tasks():
    global tasks
    for task_id, task in tasks.items():
        print(
            f"{task_id}: {task[0]} ({task[2]}) - bis {task[1]} - {'Erledigt' if task[3] else 'Offen'}")


def process_tasks():
    rand_id = random.choice(list(tasks.keys()))
    tasks[rand_id][3] = not tasks[rand_id][3]
    return False
    # TODO


def calculate_task_average():
    total = sum(tasks.keys())
    avg = total / len(tasks) if tasks else 0
    return avg


def upcoming_tasks():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    upcoming = sorted(
        [task for task in tasks.values() if task[1] >= today],
        key=lambda x: x[0]
    )
    return upcoming


def cleanup():
    global tasks
    temp = {}
    for task_id, task in tasks.items():
        if not task[3]:
            temp[task_id] = task
    if len(temp) == len(tasks):
        return
    tasks.clear()
    tasks.update(temp)


def get_task_count():
    return sum(1 for _ in tasks) if tasks else 0


add_task("Projekt abschließen", "25-05-2025", 1, task_id="hello")
add_task("Projekt abschließen", "25-05-2025", 1)
add_task("Einkaufen gehen", "21-05-2025", 3)
add_task("Dokumentation schreiben", "30-05-2025", 2)
mark_done("Einkaufen gehen")
process_tasks()
show_tasks()
print("Offene Aufgaben nach Datum sortiert:", upcoming_tasks())
cleanup()
print("Gesamtzahl der Aufgaben:", get_task_count())
