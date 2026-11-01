import pytest
from unittest.mock import patch

from ..Code.weather_service import get_weather_category


# Implementiert von: MXMR, CNStS
class TestWeatherService:
    # TDD-Zyklus 1: RED von MXMR
    # TDD-Zyklus 1: GREEN von CNStS
    # TDD-Zyklus 1: REFACTOR von MXMR & CNStS
    @pytest.mark.parametrize(
        ("temperature", "expected_category"),
        [
            (-0.1, "frostgefahr"),
            (0, "kalt"),
            (10, "kalt"),
            (10.1, "kühl"),
            (15, "kühl"),
            (15.1, "angenehm"),
            (24, "angenehm"),
            (24.1, "warm"),
            (30, "warm"),
            (30.1, "heiß"),
        ],
    )
    def test_temperature_category(self, temperature, expected_category):
        with patch("Uebung4.Code.weather_service.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"temperature": temperature}

            result = get_weather_category("Berlin")

        assert result == expected_category
        mock_get.assert_called_once_with(
            "https://api.weather.com/current?city=Berlin", timeout=5
        )
        mock_get.return_value.raise_for_status.assert_called_once_with()
