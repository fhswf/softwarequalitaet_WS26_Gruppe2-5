# Implementiert von: MXMR, CNStS
"""
Konto - einzelnes Bankkonto (Team A)

Implementiert das KontoInterface. Ein Konto kennt seine ID und seinen Saldo
und erlaubt Ein- und Auszahlungen. Ungültige Eingaben führen zu ValueError,
eine Überziehung zu RuntimeError.
"""

from decimal import Decimal
from .interfaces import KontoInterface


class Konto(KontoInterface):
    """
    Bankkonto mit fester ID und Saldo.

    Regeln:
    - ID wird bei Erstellung mitgegeben (ganze Zahl > 0)
    - Saldo und Beträge sind vom Typ Decimal und endlich
    - Anfangssaldo darf nicht negativ sein
    - Ein- und Auszahlungsbeträge müssen größer als 0 sein
    - Konto darf nicht überzogen werden (Saldo < 0), sonst RuntimeError
    """

    def __init__(self, konto_id: int, saldo: Decimal = Decimal('0.00')):
        self._validiere_konto_id(konto_id)
        self._validiere_decimal(saldo, "Saldo")
        if saldo < 0:
            raise ValueError("Anfangssaldo darf nicht negativ sein")

        self._konto_id = konto_id
        self._saldo = saldo

    # ------------------------------------------------------------------
    # Interne Hilfsmethoden (Validierung)
    # ------------------------------------------------------------------

    @staticmethod
    def _validiere_konto_id(konto_id: int) -> None:
        """Prüft, ob die Konto-ID eine ganze Zahl größer als 0 ist."""
        if isinstance(konto_id, bool) or not isinstance(konto_id, int):
            raise ValueError("Konto-ID muss eine ganze Zahl sein")
        if konto_id <= 0:
            raise ValueError("Konto-ID muss größer als 0 sein")

    @staticmethod
    def _validiere_decimal(wert: Decimal, name: str) -> None:
        """Prüft, ob ein Wert ein endlicher Decimal ist (kein float, NaN oder Infinity)."""
        if not isinstance(wert, Decimal):
            raise ValueError(f"{name} muss vom Typ Decimal sein")
        if not wert.is_finite():
            raise ValueError(f"{name} muss eine endliche Zahl sein")

    @classmethod
    def _validiere_betrag(cls, betrag: Decimal) -> None:
        """Prüft, ob ein Buchungsbetrag gültig ist (Decimal, endlich, > 0)."""
        cls._validiere_decimal(betrag, "Betrag")
        if betrag <= 0:
            raise ValueError("Betrag muss größer als 0 sein")

    # ------------------------------------------------------------------
    # Öffentliche Schnittstelle (Interface)
    # ------------------------------------------------------------------

    @property
    def konto_id(self) -> int:
        """Konto-ID (nur lesbar)."""
        return self._konto_id

    @property
    def saldo(self) -> Decimal:
        """Aktueller Saldo (nur lesbar, Änderung nur über einzahlen/auszahlen)."""
        return self._saldo

    def einzahlen(self, betrag: Decimal) -> None:
        """Erhöht den Saldo um betrag."""
        self._validiere_betrag(betrag)
        self._saldo += betrag

    def auszahlen(self, betrag: Decimal) -> None:
        """
        Verringert den Saldo um betrag.

        Würde der Saldo negativ werden, wird ein RuntimeError geworfen
        und der Saldo bleibt unverändert.
        """
        self._validiere_betrag(betrag)
        if betrag > self._saldo:
            raise RuntimeError(
                f"Auszahlung von {betrag} nicht möglich: Saldo {self._saldo} reicht nicht aus"
            )
        self._saldo -= betrag

    def __repr__(self) -> str:
        return f"Konto(konto_id={self._konto_id!r}, saldo={self._saldo!r})"
