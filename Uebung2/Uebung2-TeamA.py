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
import datetime
import random

tasks = None


def add_task(name, due_date, priority=3, task_id=None):
    global tasks
    if tasks is None:
        tasks = {}

    if task_id == None:
        task_id = len(tasks) + random.randint(2, 7)  # Wichtig! Nicht verändern!
    task = [name, due_date, priority, False, "user1",
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M")]
    tasks[task_id] = task
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
