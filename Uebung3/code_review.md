# Code-Review Übung 3 (Aufgabe 3.3)
- **Datum:** 26.10.
- **Teilnehmende:** Team A (MXMR, CNStS), Team B (SNSK, PLRS)

## Gegenseitige Erklärung
Team A – `Konto` (`Code/konto.py`)
- Konto-ID: ganze Zahl > 0 (`bool` ausgeschlossen), nur lesbar
- Saldo und Beträge: nur endliche `Decimal`-Werte, Anfangssaldo ≥ 0
- Ein- und Auszahlung: Betrag > 0, sonst `ValueError`
- Überziehung: `RuntimeError`, Saldo bleibt unverändert

Team B – `KontoService` (`Code/konto_service.py`)
- Verwaltet Konten als `List[KontoInterface]`, neue ID = größte ID + 1
- Validiert Eingaben selbst (Betrag, Anfangssaldo, Konto-ID) und delegiert Buchungen an `Konto`
- `ueberweisen`/`einziehen`: erst alles prüfen, dann auszahlen, dann einzahlen; bei Überziehung bleiben beide Konten unverändert

## Integration
- `_create_konto` liefert jetzt `Konto(konto_id, saldo)` statt `DummyKonto`.
- Relative Imports in den Tests (`from ..Code...`) funktionierten erst nach `__init__.py` in `Uebung3/`, `Code/` und `Tests/` (Commit `8f2e54a`).
- `DummyKonto` lieferte immer ID 1 und Saldo 100.00, prüfte nichts und warf keine Fehler. ID-Vergabe, Salden nach Buchungen und Überziehung ließen sich daher erst mit dem echten `Konto` testen.

## Gefundene Probleme und Lösungen
| Problem | Lösung | Stand |
|---|---|---|
| Header in Team-B-Dateien nicht im geforderten Format (`#SNSK, PLRS`) | auf `# Implementiert von: SNSK, PLRS` geändert | erledigt (`ccf116a`) |
| Service-Tests prüften weniger ungültige Beträge als die Konto-Tests (`None`, `int`, `Infinity`, `-0.01` fehlten) | `UNGUELTIGE_BETRAEGE` erweitert | erledigt (`ccf116a`) |
| Fehlende Service-Tests: `einziehen` auf dasselbe Konto, `einziehen` ohne Deckung, falscher ID-Typ bei `einzahlen`/`auszahlen`, `konto_erstellen` mit `NaN`/`Infinity` | Tests ergänzt | erledigt (`ccf116a`) |
| Validierung doppelt in `KontoService` und `Konto` | bewusst beibehalten: Prüfung läuft vor jeder Buchung (fail fast) und hängt nicht von der konkreten `KontoInterface`-Implementierung ab; Begründung als Kommentar im Code | entschieden (`ccf116a`) |
| Test `test_service_erzeugt_echte_konto_objekte` (Team A) doppelt zu `test_create_konto_liefert_echtes_konto` (Team B) | Test in `test_konto.py` entfernt | erledigt |

## Ergebnis
`pytest Uebung3/Tests/ -v`: 186 Tests bestanden.
