"""
MXMR, CNStS
"""
"""
Aufgabe 1

To-Do-Programm, Aufgaben liegen im globalen Dictionary tasks (ID -> Liste).
- add_task: Aufgabe anlegen, ID wird ggf. zufällig erzeugt
- remove_task: Aufgabe per ID löschen
- mark_done: Aufgabe per Name als erledigt markieren
- show_tasks: alle Aufgaben ausgeben
- process_tasks: Status einer zufälligen Aufgabe umdrehen
- calculate_task_average: Mittelwert der IDs (wird nie aufgerufen)
- upcoming_tasks: anstehende Aufgaben, sortiert nach Name
- cleanup: erledigte Aufgaben löschen
- get_task_count: Anzahl der Aufgaben

Was das Verständnis erschwert:
- Aufgaben sind Listen, man muss nachschauen was task[0], task[3] usw. bedeutet
- tasks startet als None, erst add_task macht ein Dictionary daraus
- ID-Erzeugung mit random und "Wichtig! Nicht verändern!" ohne Begründung
- IDs mal String ("hello"), mal int
- process_tasks: Name nichtssagend, gibt immer False zurück, TODO ohne Erklärung
- mark_done sucht über den Namen, gibt immer "Erledigt" zurück
- Ausgabe sagt "nach Datum sortiert", sortiert wird nach Name
- backup_tasks und "user1" werden nie benutzt
- keine Docstrings, keine Type Hints
"""
"""
Aufgabe 2

Positiv:
- kleine Funktionen mit meist sprechenden Namen
- remove_task gibt True/False zurück
- sinnvolle Default-Parameter (priority=3, task_id=None)

Negativ:
- random-ID kann eine vorhandene ID treffen, alte Aufgabe wird dann überschrieben
- Datum als String TT-MM-JJJJ verglichen, "30-05-2025" >= "27-09-2026" ist True
- upcoming_tasks liefert auch erledigte Aufgaben
- calculate_task_average stürzt wegen der ID "hello" ab (TypeError) sofern sie aufgerufen würde
- ohne vorheriges add_task stürzen fast alle Funktionen ab (tasks = None)
- backup_tasks teilt dieselben Listen, ist also kein Backup
- globaler Zustand und random machen das Testen schwer
- uneinheitliche Rückgabewerte (str, bool, None, immer False)
- global auch dort, wo tasks gar nicht neu zugewiesen wird
- Logik und Ausgabe vermischt (show_tasks druckt direkt)
- == None statt is None, sum(1 for _ in tasks) statt len(tasks)
- Aufrufe am Ende nicht unter if _name_ == "_main_":

Verbesserungen:
- dataclass statt Liste für Aufgaben
- datetime.date statt String fürs Datum
- fortlaufende IDs statt random
- tasks direkt als {} initialisieren
- mark_done über ID 
- upcoming_tasks nach Datum sortieren und erledigte rausfiltern
- unnötigen Code entfernen (backup_tasks, calculate_task_average)
- Logik und Ausgabe trennen
- einheitliche Rückgabewerte
- Docstrings und Type Hints ergänzen
- _main_-Block
"""
# einzelne imports statt komplette Modul
from datetime import datetime, date
# dataclass für benannte Felder
from dataclasses import dataclass, field
# random entfernt, wird nicht mehr gebraucht
from itertools import count

# dataclass mit Feldern statt Liste mit Indizes (task[0], task[3], ...)
@dataclass
class Task:
    """Eine einzelne To-Do-Aufgabe."""

    name: str
    # date statt String
    due_date: date
    priority: int = 3
    done: bool = False
    # unnötigen User entfernt
    # date statt String
    created: datetime = field(default_factory=datetime.now)

    # Eingaben prüfen, damit falsche Typen nicht erst später in upcoming_tasks abstürzen
    def __post_init__(self):
        """Prüft die Eingaben direkt beim Anlegen der Aufgabe"""
        if not self.name:
            raise ValueError("name darf nicht leer sein")
        if not isinstance(self.due_date, date) or isinstance(self.due_date, datetime):
            raise TypeError("due_date muss ein datetime.date sein")
        if self.priority not in (1, 2, 3):
            raise ValueError("priority muss 1, 2 oder 3 sein")

# task initialisiert
tasks: dict[int, Task] = {}
# fortlaufende IDs statt len(tasks) + random
_next_id = count(1)

# task_id-Parameter entfernt
# dataclass initialisiert
# type hints hinzugefügt
def add_task(name, due_date, priority=3) -> int:
    """Legt eine neue Aufgabe an und gibt ihre ID zurück
       Wirft ValueError bei leerem Namen oder ungültiger Priorität,
       TypeError wenn due_date kein date ist.
    """
    # dataclass initialisieren
    task = Task(name, due_date, priority)
    task_id = next(_next_id)
    # task_id erst nach initialisierung setzen
    tasks[task_id] = task
    return task_id

# type hints hinzugefügt
def remove_task(task_id) -> bool:
    """Entfernt eine Aufgabe und gibt True zurück, wenn sie existierte"""
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False

# Suche über ID statt name
# Rückgabe bool wie bei remove_task statt immer "Erledigt"
# type hints hinzugefügt
def mark_done(task_id) -> bool:
    """markiert eine Aufgabe als erledigt und gibt True zurück, wenn sie existierte"""
    if task_id not in tasks:
        return False
    tasks[task_id].done = True
    return True

# Logik und Ausgabe trennen
# type hints hinzugefügt
def format_tasks(task_id, task) -> str:
    """Gibt eine Aufgabe als String zurück"""
    status = "Erledigt" if task.done else "Offen"
    return f"{task_id}: {task.name} ({task.priority}) - bis {task.due_date} - {status}"

# type hints hinzugefügt
def upcoming_tasks() -> list[tuple[int, Task]]:
    """Gibt alle offenen Aufgaben mit Fälligkeit ab heute sortiert nach Datum zurück"""
    # heute als date
    today = date.today()
    # Indizes zu Attribute
    # erledigte Aufgaben rausfiltern
    # gibt IDs mit zurück, damit Ausgabe format_task nutzt
    upcoming = [(task_id, task) for task_id, task in tasks.items() if not task.done and task.due_date >= today]
    return sorted(upcoming, key=lambda item: item[1].due_date)

# kein vorzeitiges return mehr
# gibt Anzahl der entfernten Aufgaben zurück
# type hints hinzugefügt
def cleanup() -> int:
    """Entfernt alle erledigten Aufgaben und gibt die Anzahl der entfernten Aufgaben zurück"""
    done_ids = [task_id for task_id, task in tasks.items() if task.done]
    for task_id in done_ids:
        del tasks[task_id]
    return len(done_ids)


def get_task_count() -> int:
    """Gibt die Anzahl aller Aufgaben zurück"""
    # len statt sum, tasks ist nie mehr None
    return len(tasks)

# Aufrufe in main(), damit beim Import nicht ausgeführt
def main():
    """Kleines Beispielprogramm"""
    # task_id="hello" entfernt
    # date statt String
    add_task("Projekt abschließen", date(2025, 5, 25), 1)
    # date statt String
    add_task("Projekt abschließen", date(2025, 5, 25), 1)
    # date statt String
    add_task("Einkaufen gehen", date(2025, 5, 21), 3)
    # date statt String
    # Datum erhöht für Ausgabe
    add_task("Dokumentation schreiben", date(2027, 5, 30), 2)
    # ID statt String
    mark_done(3)

    # Ausgabe nur noch hier
    for task_id, task in tasks.items():
        print(format_tasks(task_id, task))

    # Ausgabe über format_task statt liste
    print("Offene Aufgaben nach Datum sortiert:")
    for task_id, task in upcoming_tasks():
        print(" ", format_tasks(task_id, task))

    # verbesserte Ausgabe
    print("Entfernte Aufgaben:", cleanup())
    print("Gesamtzahl der Aufgaben:", get_task_count())

if __name__ == "__main__":
    main()