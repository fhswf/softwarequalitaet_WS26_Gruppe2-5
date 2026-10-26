# Implementiert von: MXMR, CNStS
"""
Tests für die Konto-Klasse (Test-After Approach)
================================================

Team A - Tests nach der Konto-Implementierung.
Alle Tests folgen dem AAA-Pattern (Arrange - Act - Assert).
"""

import pytest
from decimal import Decimal

from ..Code.konto import Konto
from ..Code.interfaces import KontoInterface
from ..Code.konto_service import KontoService


# ----------------------------------------------------------------------
# Fixtures und Testdaten
# ----------------------------------------------------------------------

@pytest.fixture
def konto():
    """Konto 1 mit Saldo 100.00"""
    return Konto(1, Decimal("100.00"))


@pytest.fixture
def leeres_konto():
    """Konto 2 mit Saldo 0.00"""
    return Konto(2)


UNGUELTIGE_IDS = [0, -1, "1", "", None, 1.0, True]

UNGUELTIGE_BETRAEGE = [
    Decimal("0.00"),
    Decimal("-0.01"),
    Decimal("-10.00"),
    10.0,                 # float statt Decimal
    10,                   # int statt Decimal
    "10.00",              # String statt Decimal
    None,
    Decimal("NaN"),
    Decimal("Infinity"),
]


# ----------------------------------------------------------------------
# Aufgabe 2: Tests nach der Implementierung
# ----------------------------------------------------------------------

class TestKontoErstellung:
    """Tests für den Konstruktor"""

    def test_konto_mit_gueltiger_id_und_saldo(self):
        # Arrange
        konto_id = 1
        saldo = Decimal("100.00")

        # Act
        konto = Konto(konto_id, saldo)

        # Assert
        assert (konto.konto_id, konto.saldo) == (1, Decimal("100.00"))

    def test_konto_ohne_saldo_hat_saldo_null(self):
        # Act
        konto = Konto(1)

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_konto_mit_saldo_null(self):
        # Act
        konto = Konto(1, Decimal("0.00"))

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_konto_mit_grosser_id(self):
        # Act
        konto = Konto(10**12)

        # Assert
        assert konto.konto_id == 10**12

    @pytest.mark.parametrize("konto_id", UNGUELTIGE_IDS)
    def test_konto_mit_ungueltiger_id_wirft_value_error(self, konto_id):
        # Act / Assert
        with pytest.raises(ValueError):
            Konto(konto_id, Decimal("10.00"))

    def test_konto_mit_negativem_saldo_wirft_value_error(self):
        # Act / Assert
        with pytest.raises(ValueError, match="negativ"):
            Konto(1, Decimal("-0.01"))

    @pytest.mark.parametrize(
        "saldo", [100.0, 100, "100.00", None, Decimal("NaN"), Decimal("Infinity")]
    )
    def test_konto_mit_ungueltigem_saldo_wirft_value_error(self, saldo):
        # Act / Assert
        with pytest.raises(ValueError):
            Konto(1, saldo)


class TestKontoEigenschaften:
    """Tests für die Properties konto_id und saldo"""

    def test_konto_id_gibt_id_zurueck(self, konto):
        # Act
        konto_id = konto.konto_id

        # Assert
        assert konto_id == 1

    def test_saldo_gibt_saldo_zurueck(self, konto):
        # Act
        saldo = konto.saldo

        # Assert
        assert saldo == Decimal("100.00")

    def test_saldo_ist_decimal(self, konto):
        # Act
        saldo = konto.saldo

        # Assert
        assert isinstance(saldo, Decimal)

    def test_konto_id_ist_read_only(self, konto):
        # Act / Assert
        with pytest.raises(AttributeError):
            konto.konto_id = 2

    def test_saldo_ist_read_only(self, konto):
        # Act / Assert
        with pytest.raises(AttributeError):
            konto.saldo = Decimal("1000000.00")

    def test_saldo_ist_nach_versuchter_aenderung_unveraendert(self, konto):
        # Act
        with pytest.raises(AttributeError):
            konto.saldo = Decimal("1000000.00")

        # Assert
        assert konto.saldo == Decimal("100.00")


class TestEinzahlung:
    """Tests für einzahlen()"""

    def test_einzahlung_erhoeht_saldo(self, konto):
        # Act
        konto.einzahlen(Decimal("25.50"))

        # Assert
        assert konto.saldo == Decimal("125.50")

    def test_einzahlung_auf_leeres_konto(self, leeres_konto):
        # Act
        leeres_konto.einzahlen(Decimal("10.00"))

        # Assert
        assert leeres_konto.saldo == Decimal("10.00")

    def test_mehrere_einzahlungen_summieren_sich(self, leeres_konto):
        # Act
        for _ in range(3):
            leeres_konto.einzahlen(Decimal("10.00"))

        # Assert
        assert leeres_konto.saldo == Decimal("30.00")

    def test_einzahlung_gibt_none_zurueck(self, konto):
        # Act
        ergebnis = konto.einzahlen(Decimal("1.00"))

        # Assert
        assert ergebnis is None

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_einzahlung_mit_ungueltigem_betrag_wirft_value_error(self, konto, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            konto.einzahlen(betrag)

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_einzahlung_mit_ungueltigem_betrag_aendert_saldo_nicht(self, konto, betrag):
        # Act
        with pytest.raises(ValueError):
            konto.einzahlen(betrag)

        # Assert
        assert konto.saldo == Decimal("100.00")


class TestAuszahlung:
    """Tests für auszahlen()"""

    def test_auszahlung_reduziert_saldo(self, konto):
        # Act
        konto.auszahlen(Decimal("30.00"))

        # Assert
        assert konto.saldo == Decimal("70.00")

    def test_auszahlung_kompletter_saldo_ist_erlaubt(self, konto):
        # Act
        konto.auszahlen(Decimal("100.00"))

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_mehrere_auszahlungen(self, konto):
        # Act
        konto.auszahlen(Decimal("40.00"))
        konto.auszahlen(Decimal("60.00"))

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_auszahlung_gibt_none_zurueck(self, konto):
        # Act
        ergebnis = konto.auszahlen(Decimal("1.00"))

        # Assert
        assert ergebnis is None

    def test_auszahlung_bei_unzureichendem_saldo_wirft_runtime_error(self, konto):
        # Act / Assert
        with pytest.raises(RuntimeError):
            konto.auszahlen(Decimal("100.01"))

    def test_auszahlung_bei_unzureichendem_saldo_aendert_saldo_nicht(self, konto):
        # Act
        with pytest.raises(RuntimeError):
            konto.auszahlen(Decimal("500.00"))

        # Assert
        assert konto.saldo == Decimal("100.00")

    def test_auszahlung_von_leerem_konto_wirft_runtime_error(self, leeres_konto):
        # Act / Assert
        with pytest.raises(RuntimeError):
            leeres_konto.auszahlen(Decimal("0.01"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_auszahlung_mit_ungueltigem_betrag_wirft_value_error(self, konto, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            konto.auszahlen(betrag)

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_auszahlung_mit_ungueltigem_betrag_aendert_saldo_nicht(self, konto, betrag):
        # Act
        with pytest.raises(ValueError):
            konto.auszahlen(betrag)

        # Assert
        assert konto.saldo == Decimal("100.00")


class TestKontoGrenzfaelle:
    """Tests für Grenzfälle und Besonderheiten"""

    def test_sehr_grosser_betrag(self, leeres_konto):
        # Arrange
        betrag = Decimal("999999999999.99")

        # Act
        leeres_konto.einzahlen(betrag)

        # Assert
        assert leeres_konto.saldo == betrag

    def test_kleinster_cent_betrag_einzahlen(self, leeres_konto):
        # Act
        leeres_konto.einzahlen(Decimal("0.01"))

        # Assert
        assert leeres_konto.saldo == Decimal("0.01")

    def test_auszahlung_ein_cent_unter_saldo_ist_erlaubt(self, konto):
        # Act
        konto.auszahlen(Decimal("99.99"))

        # Assert
        assert konto.saldo == Decimal("0.01")

    def test_decimal_praezision_ohne_rundungsfehler(self, leeres_konto):
        # Act: mit float wäre 0.1 + 0.2 != 0.3
        leeres_konto.einzahlen(Decimal("0.10"))
        leeres_konto.einzahlen(Decimal("0.20"))

        # Assert
        assert leeres_konto.saldo == Decimal("0.30")

    def test_ein_und_auszahlung_gleichen_sich_aus(self, konto):
        # Act
        konto.einzahlen(Decimal("12.34"))
        konto.auszahlen(Decimal("12.34"))

        # Assert
        assert konto.saldo == Decimal("100.00")

    def test_konten_sind_unabhaengig(self, konto, leeres_konto):
        # Act
        konto.auszahlen(Decimal("50.00"))

        # Assert
        assert leeres_konto.saldo == Decimal("0.00")

    def test_repr_enthaelt_id_und_saldo(self, konto):
        # Act
        text = repr(konto)

        # Assert
        assert text == "Konto(konto_id=1, saldo=Decimal('100.00'))"


# ----------------------------------------------------------------------
# Aufgabe 4: Tests nach der Integration mit KontoService
# ----------------------------------------------------------------------

class TestKontoInterfaceVertrag:
    """Prüft, dass Konto den Vertrag aus KontoInterface einhält, auf den sich KontoService verlässt"""

    def test_konto_implementiert_interface(self, konto):
        # Assert
        assert isinstance(konto, KontoInterface)

    def test_ungueltige_eingaben_werfen_value_error_nicht_type_error(self):
        # Interface schreibt ValueError vor, auch bei falschem Typ
        # Act / Assert
        with pytest.raises(ValueError):
            Konto("abc")

    def test_ueberziehung_wirft_runtime_error_nicht_value_error(self, konto):
        # Service unterscheidet: ValueError = falsche Eingabe, RuntimeError = Überziehung
        # Act / Assert
        with pytest.raises(RuntimeError) as fehler:
            konto.auszahlen(Decimal("100.01"))
        assert not isinstance(fehler.value, ValueError)


class TestKontoImKontoService:
    """Integration: Konto-Objekte, die der KontoService über _create_konto erzeugt"""

    def test_service_erzeugt_echte_konto_objekte(self):
        # Arrange
        service = KontoService()

        # Act
        konto = service._create_konto(1, Decimal("10.00"))

        # Assert
        assert type(konto) is Konto

    def test_ueberweisung_ohne_deckung_laesst_beide_konten_unveraendert(self):
        # Arrange
        service = KontoService()
        sender = service.konto_erstellen(Decimal("20.00"))
        empfaenger = service.konto_erstellen(Decimal("5.00"))

        # Act
        with pytest.raises(RuntimeError):
            service.ueberweisen(sender, empfaenger, Decimal("20.01"))

        # Assert
        assert service.konten_auflisten() == [
            {"konto_id": sender, "saldo": Decimal("20.00")},
            {"konto_id": empfaenger, "saldo": Decimal("5.00")},
        ]

    def test_service_saldo_entspricht_konto_saldo_nach_buchungen(self):
        # Arrange
        service = KontoService()
        a = service.konto_erstellen(Decimal("100.00"))
        b = service.konto_erstellen()

        # Act
        service.ueberweisen(a, b, Decimal("33.33"))
        service.einzahlen(b, Decimal("0.67"))

        # Assert
        assert service.konten_auflisten() == [
            {"konto_id": a, "saldo": Decimal("66.67")},
            {"konto_id": b, "saldo": Decimal("34.00")},
        ]
