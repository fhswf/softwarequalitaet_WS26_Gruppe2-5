# Implementiert von: SNSK, PLRS
"""
Tests für die KontoService-Klasse (Test-After Approach)
=======================================================

Team B - Tests nach der KontoService-Implementierung.
Alle Tests folgen dem AAA-Pattern (Arrange - Act - Assert).
"""

import pytest
from decimal import Decimal

from ..Code.konto_service import KontoService
from ..Code.konto import Konto
from ..Code.interfaces import KontoServiceInterface, KontoInterface


# ----------------------------------------------------------------------
# Fixtures und Hilfsfunktionen
# ----------------------------------------------------------------------

@pytest.fixture
def service():
    """Leerer KontoService"""
    return KontoService()


@pytest.fixture
def service_mit_zwei_konten():
    """Service mit Konto 1 (100.00) und Konto 2 (50.00)"""
    service = KontoService()
    service.konto_erstellen(Decimal("100.00"))
    service.konto_erstellen(Decimal("50.00"))
    return service


def saldo_von(service: KontoService, konto_id: int) -> Decimal:
    """Liest den Saldo eines Kontos über konten_auflisten() aus."""
    for eintrag in service.konten_auflisten():
        if eintrag["konto_id"] == konto_id:
            return eintrag["saldo"]
    raise AssertionError(f"Konto {konto_id} nicht gefunden")


UNGUELTIGE_BETRAEGE = [
    Decimal("0.00"),
    Decimal("-10.00"),
    10.0,          # float statt Decimal
    "10.00",       # String statt Decimal
    Decimal("NaN"),
    Decimal("Infinity"),
    Decimal("-0.01"),
    10,            # int statt Decimal
    None,
]

UNGUELTIGE_KONTO_IDS = ["1", None, True]


class TestKontoServiceErstellung:
    """Tests für KontoService-Erstellung und Setup"""

    def test_service_implementiert_interface(self):
        # Arrange / Act
        service = KontoService()

        # Assert
        assert isinstance(service, KontoServiceInterface)

    def test_neuer_service_hat_keine_konten(self, service):
        # Act
        konten = service.konten_auflisten()

        # Assert
        assert konten == []

    def test_neuer_service_max_konto_id_ist_null(self, service):
        # Act
        max_id = service.get_max_konto_id()

        # Assert
        assert max_id == 0

    def test_neuer_service_gesamtsaldo_ist_null(self, service):
        # Act
        gesamt = service.gesamtsaldo_berechnen()

        # Assert
        assert gesamt == Decimal("0.00")


class TestKontoVerwaltung:
    """Tests für Konto-Erstellung und -Verwaltung"""

    def test_konto_erstellen_erstes_konto_bekommt_id_eins(self, service):
        # Act
        konto_id = service.konto_erstellen(Decimal("10.00"))

        # Assert
        assert konto_id == 1

    def test_konto_erstellen_ohne_saldo_hat_saldo_null(self, service):
        # Act
        konto_id = service.konto_erstellen()

        # Assert
        assert saldo_von(service, konto_id) == Decimal("0.00")

    def test_konto_erstellen_uebernimmt_anfangssaldo(self, service):
        # Arrange
        anfangssaldo = Decimal("123.45")

        # Act
        konto_id = service.konto_erstellen(anfangssaldo)

        # Assert
        assert saldo_von(service, konto_id) == anfangssaldo

    def test_konto_erstellen_vergibt_fortlaufende_ids(self, service):
        # Act
        ids = [service.konto_erstellen() for _ in range(3)]

        # Assert
        assert ids == [1, 2, 3]

    def test_konto_erstellen_fuegt_konto_zur_liste_hinzu(self, service):
        # Act
        service.konto_erstellen(Decimal("10.00"))

        # Assert
        assert len(service.konten_auflisten()) == 1

    def test_konto_erstellen_mit_negativem_saldo_wirft_value_error(self, service):
        # Act / Assert
        with pytest.raises(ValueError):
            service.konto_erstellen(Decimal("-0.01"))

    @pytest.mark.parametrize("saldo", [100.0, 100, "100.00", None])
    def test_konto_erstellen_mit_falschem_typ_wirft_value_error(self, service, saldo):
        # Act / Assert
        with pytest.raises(ValueError):
            service.konto_erstellen(saldo)

    def test_konto_erstellen_mit_ungueltigem_saldo_legt_kein_konto_an(self, service):
        # Act
        with pytest.raises(ValueError):
            service.konto_erstellen(Decimal("-5.00"))

        # Assert
        assert service.konten_auflisten() == []

    @pytest.mark.parametrize("saldo", [Decimal("NaN"), Decimal("Infinity")])
    def test_konto_erstellen_mit_nicht_endlichem_saldo_wirft_value_error(self, service, saldo):
        # Act / Assert
        with pytest.raises(ValueError):
            service.konto_erstellen(saldo)

    @pytest.mark.parametrize("saldo", [Decimal("NaN"), Decimal("Infinity")])
    def test_konto_erstellen_mit_nicht_endlichem_saldo_legt_kein_konto_an(self, service, saldo):
        # Act
        with pytest.raises(ValueError):
            service.konto_erstellen(saldo)

        # Assert
        assert service.konten_auflisten() == []

    def test_konten_auflisten_liefert_id_und_saldo(self, service):
        # Arrange
        service.konto_erstellen(Decimal("42.00"))

        # Act
        konten = service.konten_auflisten()

        # Assert
        assert konten == [{"konto_id": 1, "saldo": Decimal("42.00")}]

    def test_konten_auflisten_liefert_alle_konten_in_reihenfolge(self, service_mit_zwei_konten):
        # Act
        konten = service_mit_zwei_konten.konten_auflisten()

        # Assert
        assert [k["konto_id"] for k in konten] == [1, 2]

    def test_create_konto_liefert_echtes_konto(self, service):
        # Act
        konto = service._create_konto(7, Decimal("10.00"))

        # Assert
        assert isinstance(konto, Konto)
        assert isinstance(konto, KontoInterface)

    def test_create_konto_uebernimmt_id_und_saldo(self, service):
        # Act
        konto = service._create_konto(7, Decimal("10.00"))

        # Assert
        assert (konto.konto_id, konto.saldo) == (7, Decimal("10.00"))


class TestTransaktionen:
    """Tests für Transaktions-Funktionen"""

    # --- einzahlen ---

    def test_einzahlen_erhoeht_saldo(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.einzahlen(1, Decimal("25.50"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("125.50")

    def test_einzahlen_aendert_andere_konten_nicht(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.einzahlen(1, Decimal("25.50"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 2) == Decimal("50.00")

    def test_einzahlen_auf_unbekanntes_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einzahlen(99, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_einzahlen_mit_ungueltigem_betrag_wirft_value_error(self, service_mit_zwei_konten, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einzahlen(1, betrag)

    @pytest.mark.parametrize("konto_id", UNGUELTIGE_KONTO_IDS)
    def test_einzahlen_mit_ungueltiger_konto_id_wirft_value_error(self, service_mit_zwei_konten, konto_id):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einzahlen(konto_id, Decimal("10.00"))

    # --- auszahlen ---

    def test_auszahlen_reduziert_saldo(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.auszahlen(1, Decimal("30.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("70.00")

    def test_auszahlen_kompletter_saldo_ist_erlaubt(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.auszahlen(1, Decimal("100.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("0.00")

    def test_auszahlen_bei_unzureichendem_saldo_wirft_runtime_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.auszahlen(1, Decimal("100.01"))

    def test_auszahlen_bei_unzureichendem_saldo_aendert_saldo_nicht(self, service_mit_zwei_konten):
        # Act
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.auszahlen(1, Decimal("500.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("100.00")

    def test_auszahlen_von_unbekanntem_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.auszahlen(99, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_auszahlen_mit_ungueltigem_betrag_wirft_value_error(self, service_mit_zwei_konten, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.auszahlen(1, betrag)

    @pytest.mark.parametrize("konto_id", UNGUELTIGE_KONTO_IDS)
    def test_auszahlen_mit_ungueltiger_konto_id_wirft_value_error(self, service_mit_zwei_konten, konto_id):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.auszahlen(konto_id, Decimal("10.00"))

    # --- ueberweisen ---

    def test_ueberweisen_reduziert_sender_saldo(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.ueberweisen(1, 2, Decimal("40.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("60.00")

    def test_ueberweisen_erhoeht_empfaenger_saldo(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.ueberweisen(1, 2, Decimal("40.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 2) == Decimal("90.00")

    def test_ueberweisen_aendert_gesamtsaldo_nicht(self, service_mit_zwei_konten):
        # Arrange
        vorher = service_mit_zwei_konten.gesamtsaldo_berechnen()

        # Act
        service_mit_zwei_konten.ueberweisen(1, 2, Decimal("40.00"))

        # Assert
        assert service_mit_zwei_konten.gesamtsaldo_berechnen() == vorher

    def test_ueberweisen_bei_unzureichendem_saldo_wirft_runtime_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.ueberweisen(2, 1, Decimal("50.01"))

    def test_ueberweisen_bei_unzureichendem_saldo_aendert_keine_salden(self, service_mit_zwei_konten):
        # Act
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.ueberweisen(2, 1, Decimal("50.01"))

        # Assert
        assert (saldo_von(service_mit_zwei_konten, 1), saldo_von(service_mit_zwei_konten, 2)) == (
            Decimal("100.00"),
            Decimal("50.00"),
        )

    def test_ueberweisen_an_unbekanntes_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(1, 99, Decimal("10.00"))

    def test_ueberweisen_an_unbekanntes_konto_aendert_sender_nicht(self, service_mit_zwei_konten):
        # Act
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(1, 99, Decimal("10.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("100.00")

    def test_ueberweisen_von_unbekanntem_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(99, 1, Decimal("10.00"))

    def test_ueberweisen_auf_dasselbe_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(1, 1, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_ueberweisen_mit_ungueltigem_betrag_wirft_value_error(self, service_mit_zwei_konten, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(1, 2, betrag)

    @pytest.mark.parametrize("konto_id", ["1", 1.0, None, True])
    def test_ueberweisen_mit_ungueltiger_konto_id_wirft_value_error(self, service_mit_zwei_konten, konto_id):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.ueberweisen(konto_id, 2, Decimal("10.00"))

    # --- einziehen ---

    def test_einziehen_belastet_zahlendes_konto(self, service_mit_zwei_konten):
        # Act: Konto 2 zieht 30.00 von Konto 1 ein
        service_mit_zwei_konten.einziehen(1, 2, Decimal("30.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("70.00")

    def test_einziehen_schreibt_einziehendem_konto_gut(self, service_mit_zwei_konten):
        # Act
        service_mit_zwei_konten.einziehen(1, 2, Decimal("30.00"))

        # Assert
        assert saldo_von(service_mit_zwei_konten, 2) == Decimal("80.00")

    def test_einziehen_bei_unzureichendem_saldo_wirft_runtime_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.einziehen(2, 1, Decimal("60.00"))

    def test_einziehen_bei_unzureichendem_saldo_aendert_keine_salden(self, service_mit_zwei_konten):
        # Act
        with pytest.raises(RuntimeError):
            service_mit_zwei_konten.einziehen(2, 1, Decimal("60.00"))

        # Assert
        assert (saldo_von(service_mit_zwei_konten, 1), saldo_von(service_mit_zwei_konten, 2)) == (
            Decimal("100.00"),
            Decimal("50.00"),
        )

    def test_einziehen_auf_dasselbe_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einziehen(1, 1, Decimal("10.00"))

    def test_einziehen_von_unbekanntem_konto_wirft_value_error(self, service_mit_zwei_konten):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einziehen(99, 1, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_einziehen_mit_ungueltigem_betrag_wirft_value_error(self, service_mit_zwei_konten, betrag):
        # Act / Assert
        with pytest.raises(ValueError):
            service_mit_zwei_konten.einziehen(1, 2, betrag)


class TestSaldoFunktionen:
    """Tests für gesamtsaldo_berechnen()"""

    def test_gesamtsaldo_mit_einem_konto(self, service):
        # Arrange
        service.konto_erstellen(Decimal("80.25"))

        # Act
        gesamt = service.gesamtsaldo_berechnen()

        # Assert
        assert gesamt == Decimal("80.25")

    def test_gesamtsaldo_mit_mehreren_konten(self, service_mit_zwei_konten):
        # Act
        gesamt = service_mit_zwei_konten.gesamtsaldo_berechnen()

        # Assert
        assert gesamt == Decimal("150.00")

    def test_gesamtsaldo_ist_decimal(self, service_mit_zwei_konten):
        # Act
        gesamt = service_mit_zwei_konten.gesamtsaldo_berechnen()

        # Assert
        assert isinstance(gesamt, Decimal)

    def test_gesamtsaldo_beruecksichtigt_einzahlung(self, service_mit_zwei_konten):
        # Arrange
        service_mit_zwei_konten.einzahlen(2, Decimal("0.01"))

        # Act
        gesamt = service_mit_zwei_konten.gesamtsaldo_berechnen()

        # Assert
        assert gesamt == Decimal("150.01")


class TestUtilityFunktionen:
    """Tests für ID-Verwaltung (get_max_konto_id) und Export (konten_auflisten)"""

    def test_max_konto_id_nach_einem_konto_ist_eins(self, service):
        # Arrange
        service.konto_erstellen()

        # Act
        max_id = service.get_max_konto_id()

        # Assert
        assert max_id == 1

    def test_max_konto_id_entspricht_letzter_vergebener_id(self, service):
        # Arrange
        for _ in range(3):
            letzte_id = service.konto_erstellen()

        # Act
        max_id = service.get_max_konto_id()

        # Assert
        assert max_id == letzte_id == 3

    def test_vergebene_ids_sind_eindeutig(self, service):
        # Arrange
        for _ in range(5):
            service.konto_erstellen()

        # Act
        ids = [k["konto_id"] for k in service.konten_auflisten()]

        # Assert
        assert len(ids) == len(set(ids))

    # --- Export (konten_auflisten) ---

    def test_export_aendern_der_liste_beeinflusst_service_nicht(self, service_mit_zwei_konten):
        # Arrange
        export = service_mit_zwei_konten.konten_auflisten()

        # Act
        export.clear()

        # Assert
        assert len(service_mit_zwei_konten.konten_auflisten()) == 2

    def test_export_aendern_eines_eintrags_beeinflusst_saldo_nicht(self, service_mit_zwei_konten):
        # Arrange
        export = service_mit_zwei_konten.konten_auflisten()

        # Act
        export[0]["saldo"] = Decimal("999999.00")

        # Assert
        assert saldo_von(service_mit_zwei_konten, 1) == Decimal("100.00")

    def test_export_spiegelt_aktuellen_stand_nach_buchung(self, service_mit_zwei_konten):
        # Arrange
        service_mit_zwei_konten.ueberweisen(1, 2, Decimal("10.00"))

        # Act
        export = service_mit_zwei_konten.konten_auflisten()

        # Assert
        assert [k["saldo"] for k in export] == [Decimal("90.00"), Decimal("60.00")]


class TestKontoServiceIntegration:
    """Integration-Tests zwischen Service und echter Konto-Klasse"""

    def test_vollstaendiger_workflow(self):
        # Arrange
        service = KontoService()
        a = service.konto_erstellen(Decimal("200.00"))
        b = service.konto_erstellen()
        c = service.konto_erstellen(Decimal("10.00"))

        # Act
        service.einzahlen(b, Decimal("50.00"))
        service.ueberweisen(a, b, Decimal("75.00"))
        service.einziehen(b, c, Decimal("25.00"))
        service.auszahlen(c, Decimal("5.00"))

        # Assert
        assert service.konten_auflisten() == [
            {"konto_id": a, "saldo": Decimal("125.00")},
            {"konto_id": b, "saldo": Decimal("100.00")},
            {"konto_id": c, "saldo": Decimal("30.00")},
        ]
        assert service.gesamtsaldo_berechnen() == Decimal("255.00")
