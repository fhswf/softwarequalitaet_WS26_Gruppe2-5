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

# Indizes der Felder in einer Aufgaben-Liste
NAME = 0
DUE_DATE = 1
PRIORITY = 2
DONE = 3
OWNER = 4
CREATED_AT = 5

DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = "%d-%m-%Y %H:%M"

# 1 = höchste, 3 = niedrigste Priorität
HIGHEST_PRIORITY = 1
LOWEST_PRIORITY = 3
DEFAULT_PRIORITY = LOWEST_PRIORITY

DEFAULT_OWNER = "user1"

STATUS_DONE = "Erledigt"
STATUS_OPEN = "Offen"

# Zufallsanteil der ID, aus dem Original übernommen
MIN_ID_OFFSET = 2
MAX_ID_OFFSET = 7

tasks = None
backup_tasks = {}


def add_task(name, due_date, priority=DEFAULT_PRIORITY, task_id=None):
    global tasks
    if tasks is None:
        tasks = {}

    if task_id is None:
        task_id = len(tasks) + random.randint(MIN_ID_OFFSET, MAX_ID_OFFSET)
    task = [name, due_date, priority, False, DEFAULT_OWNER,
            datetime.datetime.now().strftime(DATETIME_FORMAT)]
    tasks[task_id] = task
    backup_tasks[task_id] = task
    return task_id


def remove_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


def mark_done(task_name):
    for task in tasks.values():
        if task[NAME] == task_name:
            task[DONE] = True
    return STATUS_DONE


def show_tasks():
    for task_id, task in tasks.items():
        status = STATUS_DONE if task[DONE] else STATUS_OPEN
        print(f"{task_id}: {task[NAME]} ({task[PRIORITY]}) "
              f"- bis {task[DUE_DATE]} - {status}")


def process_tasks():
    rand_id = random.choice(list(tasks.keys()))
    tasks[rand_id][DONE] = not tasks[rand_id][DONE]
    return False
    # TODO


def calculate_task_average():
    total = sum(tasks.keys())
    avg = total / len(tasks) if tasks else 0
    return avg


def upcoming_tasks():
    today = datetime.datetime.now().strftime(DATE_FORMAT)
    upcoming = sorted(
        [task for task in tasks.values() if task[DUE_DATE] >= today],
        key=lambda x: x[NAME]
    )
    return upcoming


def cleanup():
    temp = {}
    for task_id, task in tasks.items():
        if not task[DONE]:
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