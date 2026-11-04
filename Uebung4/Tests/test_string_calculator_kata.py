import pytest

from ..Code.string_calculator_kata import add


class TestStringCalculatorTDD:
    # TDD-Zyklus 1: RED von PLRS (04.11.2026, 16:17)
    # TDD-Zyklus 1: GREEN von SNSK (04.11.2026, 16:21)
    def test_empty_string_returns_zero(self):
        assert add("") == 0

    # TDD-Zyklus 2: RED von SNSK (04.11.2026, 16:22)
    # TDD-Zyklus 2: GREEN von PLRS (04.11.2026, 16:23)
    def test_single_number_returns_itself(self):
        assert add("1") == 1

    # TDD-Zyklus 3: RED von PLRS (04.11.2026, 16:24)
    # TDD-Zyklus 3: GREEN von SNSK (04.11.2026, 16:25)
    def test_two_numbers_comma_separated(self):
        assert add("1,2") == 3

    # TDD-Zyklus 4: RED von SNSK (04.11.2026, 16:26)
    # TDD-Zyklus 4: GREEN von PLRS (04.11.2026, 16:27)
    # TDD-Zyklus 4: REFACTOR von PLRS & SNSK (04.11.2026, 16:28)
    def test_many_numbers(self):
        assert add("1,2,3,4,5") == 15

    # TDD-Zyklus 5: RED von PLRS (04.11.2026, 16:29)
    # TDD-Zyklus 5: GREEN von SNSK (04.11.2026, 16:30)
    # TDD-Zyklus 5: REFACTOR von PLRS & SNSK (04.11.2026, 16:32)
    def test_newline_as_delimiter(self):
        assert add("1\n2,3") == 6

    # TDD-Zyklus 6: RED von SNSK (04.11.2026, 16:33)
    def test_only_newlines_as_delimiter(self):
        assert add("1\n2\n3") == 6

    # TDD-Zyklus 7: RED von PLRS (04.11.2026, 16:34)
    def test_multi_digit_numbers(self):
        assert add("10,20") == 30

    # TDD-Zyklus 8: RED von SNSK (04.11.2026, 16:35)
    def test_zero_is_allowed(self):
        assert add("0,5") == 5


class TestStringCalculatorErweitert:
    # TDD-Zyklus 9: RED von PLRS (04.11.2026, 16:36)
    # TDD-Zyklus 9: GREEN von SNSK (04.11.2026, 16:37)
    def test_negative_number_raises_value_error(self):
        with pytest.raises(ValueError):
            add("-1")

    # TDD-Zyklus 10: RED von SNSK (04.11.2026, 16:38)
    # TDD-Zyklus 10: GREEN von PLRS (04.11.2026, 16:39)
    def test_error_message_lists_all_negatives(self):
        with pytest.raises(ValueError) as exc:
            add("1,-2,3,-4")
        assert "-2" in str(exc.value)
        assert "-4" in str(exc.value)

    # TDD-Zyklus 11: RED von PLRS (04.11.2026, 16:40)
    # TDD-Zyklus 11: REFACTOR von PLRS & SNSK (04.11.2026, 16:41)
    def test_error_message_does_not_list_positives(self):
        with pytest.raises(ValueError) as exc:
            add("1,-2,3")
        assert "-2" in str(exc.value)
        assert "3" not in str(exc.value)

    # TDD-Zyklus 12: RED von SNSK (04.11.2026, 16:42)
    # TDD-Zyklus 12: GREEN von PLRS (04.11.2026, 16:43)
    def test_numbers_over_1000_are_ignored(self):
        assert add("2,1001") == 2

    # TDD-Zyklus 13: RED von PLRS (04.11.2026, 16:44)
    def test_1000_is_still_counted(self):
        assert add("2,1000") == 1002

    # TDD-Zyklus 14: RED von SNSK (04.11.2026, 16:45)
    # TDD-Zyklus 14: REFACTOR von SNSK & PLRS (04.11.2026, 16:46)
    def test_only_big_numbers_returns_zero(self):
        assert add("1001,2000") == 0

    # TDD-Zyklus 15: RED von PLRS (04.11.2026, 16:47)
    # TDD-Zyklus 15: GREEN von SNSK (04.11.2026, 16:49)
    # TDD-Zyklus 15: REFACTOR von PLRS & SNSK (04.11.2026, 16:50)
    def test_custom_delimiter(self):
        assert add("//;\n1;2") == 3

    # TDD-Zyklus 16: RED von SNSK (04.11.2026, 16:51)
    def test_custom_delimiter_with_three_numbers(self):
        assert add("//|\n1|2|3") == 6

    # TDD-Zyklus 17: RED von PLRS (04.11.2026, 16:52)
    # TDD-Zyklus 17: REFACTOR von SNSK & PLRS (04.11.2026, 16:53)
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("", 0),
            ("5", 5),
            ("1,1", 2),
            ("1\n1", 2),
            ("1,2\n3", 6),
            ("999,1,1000", 2000),
        ],
    )
    def test_parametrized_examples(self, text, expected):
        assert add(text) == expected
