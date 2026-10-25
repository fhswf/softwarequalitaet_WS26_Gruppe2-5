#SNSK, PLRS
"""
KontoService - Verwaltung mehrerer Konten (Team B)

Implementiert das KontoServiceInterface. Der Service verwaltet die Konten,
validiert Benutzereingaben und delegiert die eigentlichen Buchungen an die
Konto-Objekte (KontoInterface).
"""

from decimal import Decimal
from typing import List, Dict

from .interfaces import KontoServiceInterface, KontoInterface
from .konto import Konto


class KontoService(KontoServiceInterface):
    """
    Verwaltet Konten als List[KontoInterface].

    Regeln:
    - Neue Konto-ID = größte vorhandene Konto-ID + 1 (erste ID ist 1)
    - Beträge müssen vom Typ Decimal und größer als 0 sein, sonst ValueError
    - Unbekannte Konto-IDs führen zu ValueError
    - Überziehung führt zu RuntimeError (wird von Konto.auszahlen geworfen)
    """

    def __init__(self):
        self._konten: List[KontoInterface] = []

    def _create_konto(self, konto_id: int, saldo: Decimal) -> KontoInterface:
        """Factory-Methode: erzeugt nach der Integration echte Konto-Objekte (Team A)."""
        return Konto(konto_id, saldo)

    # ------------------------------------------------------------------
    # Interne Hilfsmethoden (Validierung)
    # ------------------------------------------------------------------

    @staticmethod
    def _validiere_betrag(betrag: Decimal) -> None:
        """Prüft, ob ein Buchungsbetrag gültig ist (Decimal, endlich, > 0)."""
        if not isinstance(betrag, Decimal):
            raise ValueError("Betrag muss vom Typ Decimal sein")
        if not betrag.is_finite():
            raise ValueError("Betrag muss eine endliche Zahl sein")
        if betrag <= 0:
            raise ValueError("Betrag muss größer als 0 sein")

    @staticmethod
    def _validiere_anfangssaldo(saldo: Decimal) -> None:
        """Prüft, ob ein Anfangssaldo gültig ist (Decimal, endlich, >= 0)."""
        if not isinstance(saldo, Decimal):
            raise ValueError("Saldo muss vom Typ Decimal sein")
        if not saldo.is_finite():
            raise ValueError("Saldo muss eine endliche Zahl sein")
        if saldo < 0:
            raise ValueError("Anfangssaldo darf nicht negativ sein")

    def _finde_konto(self, konto_id: int) -> KontoInterface:
        """Liefert das Konto zur ID oder wirft ValueError."""
        if isinstance(konto_id, bool) or not isinstance(konto_id, int):
            raise ValueError("Konto-ID muss eine ganze Zahl sein")
        for konto in self._konten:
            if konto.konto_id == konto_id:
                return konto
        raise ValueError(f"Konto mit ID {konto_id} existiert nicht")

    def _buchen(self, von_konto_id: int, zu_konto_id: int, betrag: Decimal) -> None:
        """
        Bucht einen Betrag von einem Konto auf ein anderes.

        Erst wird alles validiert, dann zuerst ausgezahlt und danach eingezahlt.
        Scheitert die Auszahlung (z. B. Überziehung), bleiben beide Konten unverändert.
        """
        self._validiere_betrag(betrag)
        quelle = self._finde_konto(von_konto_id)
        ziel = self._finde_konto(zu_konto_id)
        if von_konto_id == zu_konto_id:
            raise ValueError("Quell- und Zielkonto dürfen nicht identisch sein")

        quelle.auszahlen(betrag)
        ziel.einzahlen(betrag)

    # ------------------------------------------------------------------
    # Öffentliche Methoden (Interface)
    # ------------------------------------------------------------------

    def konten_auflisten(self) -> List[Dict]:
        """Liefert alle Konten als Liste von Dicts mit 'konto_id' und 'saldo'."""
        return [
            {"konto_id": konto.konto_id, "saldo": konto.saldo}
            for konto in self._konten
        ]

    def konto_erstellen(self, saldo: Decimal = Decimal("0.00")) -> int:
        """Legt ein neues Konto an und gibt dessen ID zurück."""
        self._validiere_anfangssaldo(saldo)
        konto_id = self.get_max_konto_id() + 1
        konto = self._create_konto(konto_id, saldo)
        self._konten.append(konto)
        return konto_id

    def ueberweisen(self, von_konto_id: int, zu_konto_id: int, betrag: Decimal) -> None:
        """Überweist betrag von von_konto_id an zu_konto_id (vom Zahler ausgelöst)."""
        self._buchen(von_konto_id, zu_konto_id, betrag)

    def einziehen(self, von_konto_id: int, zu_konto_id: int, betrag: Decimal) -> None:
        """
        Zieht betrag von von_konto_id ein und schreibt ihn zu_konto_id gut.

        Der Geldfluss ist derselbe wie bei einer Überweisung. Der Unterschied liegt nur
        darin, wer die Buchung auslöst (hier der Empfänger, z. B. per Lastschrift).
        """
        self._buchen(von_konto_id, zu_konto_id, betrag)

    def get_max_konto_id(self) -> int:
        """Größte vorhandene Konto-ID oder 0, wenn keine Konten existieren."""
        return max((konto.konto_id for konto in self._konten), default=0)

    def gesamtsaldo_berechnen(self) -> Decimal:
        """Summe aller Kontosalden (0.00 bei leerer Kontenliste)."""
        return sum((konto.saldo for konto in self._konten), Decimal("0.00"))

    # ------------------------------------------------------------------
    # Zusätzliche Methoden (nicht im Interface, aber im Test-Template erwartet)
    # ------------------------------------------------------------------

    def einzahlen(self, konto_id: int, betrag: Decimal) -> None:
        """Zahlt betrag auf das Konto mit konto_id ein."""
        self._validiere_betrag(betrag)
        self._finde_konto(konto_id).einzahlen(betrag)

    def auszahlen(self, konto_id: int, betrag: Decimal) -> None:
        """Zahlt betrag vom Konto mit konto_id aus (RuntimeError bei Überziehung)."""
        self._validiere_betrag(betrag)
        self._finde_konto(konto_id).auszahlen(betrag)
