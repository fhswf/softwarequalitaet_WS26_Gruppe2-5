"""
TDD-Template für FizzBuzz Kata
==============================

FizzBuzz-Regeln:
- Zahl durch 3 teilbar → "Fizz"  
- Zahl durch 5 teilbar → "Buzz"
- Zahl durch 3 UND 5 teilbar → "FizzBuzz"
- Sonst → Zahl als String

TDD-Prozess: RED → GREEN → REFACTOR → wiederholen!

Autorschaft dokumentieren: Wer hat welchen TDD-Schritt gemacht?
"""
# Implementiert von: MXMR, CNStS
import pytest

from ..Code.fizzbuzz_kata import fizzbuzz


class TestFizzBuzzTDD:
    """
    Tipps:
    - Startet mit dem einfachsten Test
    - Schreibt minimalen Code zum Bestehen
    - Refaktoriert wenn nötig
    - Ein Test nach dem anderen!
    """

    # TDD-Zyklus 1: RED von MXMR
    # TDD-Zyklus 1: GREEN von CNStS
    # TDD-Zyklus 1: REFACTOR von MXMR & CNStS
    def test_eins_ergibt_eins_als_string(self):
        """Einfachster Fall: nicht durch 3 oder 5 teilbar → Zahl als String."""
        assert fizzbuzz(1) == "1"

    # TDD-Zyklus 2: RED von CNStS
    # TDD-Zyklus 2: GREEN von MXMR
    # TDD-Zyklus 2: REFACTOR von MXMR & CNStS
    def test_drei_ergibt_fizz(self):
        """Durch 3 teilbar → "Fizz"."""
        assert fizzbuzz(3) == "Fizz"

    # TDD-Zyklus 3: RED von MXMR
    # TDD-Zyklus 3: GREEN von CNStS
    # TDD-Zyklus 3: REFACTOR von MXMR & CNStS
    def test_fuenf_ergibt_buzz(self):
        """Durch 5 teilbar → "Buzz"."""
        assert fizzbuzz(5) == "Buzz"

    # TDD-Zyklus 4: RED von CNStS
    # TDD-Zyklus 4: GREEN von MXMR
    # TDD-Zyklus 4: REFACTOR von MXMR & CNStS
    def test_fuenfzehn_ergibt_fizzbuzz(self):
        """Durch 3 und 5 teilbar → "FizzBuzz"."""
        assert fizzbuzz(15) == "FizzBuzz"


class TestFizzBuzzErweitert:

    # TDD-Zyklus 5: RED von MXMR
    # TDD-Zyklus 5: GREEN von CNStS
    # TDD-Zyklus 5: REFACTOR von MXMR & CNStS
    @pytest.mark.parametrize("n", [0, -1, -3, -15])
    def test_nicht_positive_zahl_wirft_value_error(self, n):
        """Nur positive Ganzzahlen erlaubt (siehe Docstring) → sonst ValueError."""
        with pytest.raises(ValueError):
            fizzbuzz(n)

    # TDD-Zyklus 6: RED von CNStS
    # TDD-Zyklus 6: GREEN von MXMR
    # TDD-Zyklus 6: REFACTOR von MXMR & CNStS
    @pytest.mark.parametrize("n", [3.0, 7.5, True])
    def test_keine_ganzzahl_wirft_type_error(self, n):
        """Nur Ganzzahlen erlaubt (siehe Docstring) → Float/Bool ergibt TypeError."""
        with pytest.raises(TypeError):
            fizzbuzz(n)

    # TDD-Zyklus 7: RED von MXMR
    # TDD-Zyklus 7: GREEN von CNStS
    # TDD-Zyklus 7: REFACTOR von MXMR & CNStS
    @pytest.mark.parametrize("n", [0.5, -2.5, False, "3", None])
    def test_typ_wird_vor_wertebereich_geprueft(self, n):
        """Falscher Typ ergibt immer den eigenen TypeError – auch bei Werten < 1."""
        with pytest.raises(TypeError, match="n muss int sein"):
            fizzbuzz(n)
