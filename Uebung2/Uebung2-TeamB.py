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
from dataclasses import dataclass, field
from itertools import count

DATE_FORMAT = "%d-%m-%Y"

# 1 = höchste, 3 = niedrigste Priorität
HIGHEST_PRIORITY = 1
LOWEST_PRIORITY = 3
DEFAULT_PRIORITY = LOWEST_PRIORITY

DEFAULT_OWNER = "user1"

STATUS_DONE = "Erledigt"
STATUS_OPEN = "Offen"


@dataclass
class Task:
    name: str
    due_date: datetime.date
    priority: int = DEFAULT_PRIORITY
    done: bool = False
    owner: str = DEFAULT_OWNER
    created_at: datetime.datetime = field(
        default_factory=datetime.datetime.now)


tasks = {}
_next_id = count(start=1)


def add_task(name, due_date, priority=DEFAULT_PRIORITY):
    if not name.strip():
        raise ValueError("Der Name darf nicht leer sein.")
    if not HIGHEST_PRIORITY <= priority <= LOWEST_PRIORITY:
        raise ValueError(f"Priorität muss zwischen {HIGHEST_PRIORITY} "
                         f"und {LOWEST_PRIORITY} liegen.")
    # wirft ValueError bei ungültigem Datum oder Format
    parsed_date = datetime.datetime.strptime(due_date, DATE_FORMAT).date()

    task_id = next(_next_id)
    tasks[task_id] = Task(name, parsed_date, priority)
    return task_id


def remove_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


def mark_done(task_id):
    task = tasks.get(task_id)
    if task is None:
        return False
    task.done = True
    return True


def show_tasks():
    for task_id, task in tasks.items():
        status = STATUS_DONE if task.done else STATUS_OPEN
        due = task.due_date.strftime(DATE_FORMAT)
        print(f"{task_id}: {task.name} ({task.priority}) "
              f"- bis {due} - {status}")


def average_priority():
    if not tasks:
        return 0.0
    return sum(task.priority for task in tasks.values()) / len(tasks)


def upcoming_tasks():
    today = datetime.date.today()
    open_tasks = [task for task in tasks.values()
                  if not task.done and task.due_date >= today]
    return sorted(open_tasks,
                  key=lambda task: (task.due_date, task.priority))


def remove_done_tasks():
    done_ids = [task_id for task_id, task in tasks.items() if task.done]
    for task_id in done_ids:
        del tasks[task_id]
    return len(done_ids)


def get_task_count():
    return len(tasks)


add_task("Projekt abschließen", "25-05-2027", 1)
shopping_id = add_task("Einkaufen gehen", "21-05-2027", 3)
add_task("Dokumentation schreiben", "30-05-2027", 2)
add_task("Steuererklärung", "31-07-2025", 1)
mark_done(shopping_id)
show_tasks()
print("Offene Aufgaben nach Datum sortiert:", upcoming_tasks())
print("Durchschnittliche Priorität:", average_priority())
print("Gelöschte erledigte Aufgaben:", remove_done_tasks())
print("Gesamtzahl der Aufgaben:", get_task_count())