from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
import requests

from ..Code.currency_service import assess_rate, get_exchange_rate_assessment


@pytest.fixture
def mock_get():
    with patch("requests.get") as mocked:
        yield mocked


def _mock_rate(mock_get, rate):
    mock_get.return_value.json.return_value = {"rate": rate}


def _fake_currency_api(url, **kwargs):
    rates = {
        ("EUR", "USD"): 1.05,
        ("EUR", "GBP"): 0.85,
        ("USD", "EUR"): 0.95,
    }
    query = parse_qs(urlparse(url).query)
    pair = (query["from"][0], query["to"][0])

    response = MagicMock()
    response.json.return_value = {"rate": rates.get(pair, 1.15)}
    return response


class TestCurrencyServiceBewertungen:
    # TDD-Zyklus 1: RED von SNSK (04.11.2026, 17:12)
    # TDD-Zyklus 1: GREEN von PLRS (04.11.2026, 17:17)
    def test_fair_rate(self, mock_get):
        _mock_rate(mock_get, 1.05)

        result = get_exchange_rate_assessment("EUR", "USD")

        assert result == "fair"
        mock_get.assert_called_once()

    # TDD-Zyklus 2: RED von PLRS (04.11.2026, 17:19)
    # TDD-Zyklus 2: GREEN von SNSK (04.11.2026, 17:21)
    def test_very_unfavorable_rate(self, mock_get):
        _mock_rate(mock_get, 0.85)
        assert get_exchange_rate_assessment("EUR", "USD") == "sehr ungünstig"

    # TDD-Zyklus 3: RED von SNSK (04.11.2026, 17:22)
    # TDD-Zyklus 3: GREEN von PLRS (04.11.2026, 17:23)
    def test_unfavorable_rate(self, mock_get):
        _mock_rate(mock_get, 0.95)
        assert get_exchange_rate_assessment("EUR", "USD") == "ungünstig"

    # TDD-Zyklus 4: RED von PLRS (04.11.2026, 17:24)
    # TDD-Zyklus 4: GREEN von SNSK (04.11.2026, 17:25)
    def test_favorable_rate(self, mock_get):
        _mock_rate(mock_get, 1.15)
        assert get_exchange_rate_assessment("EUR", "USD") == "günstig"

    # TDD-Zyklus 5: RED von SNSK (04.11.2026, 17:26)
    # TDD-Zyklus 5: GREEN von PLRS (04.11.2026, 17:27)
    # TDD-Zyklus 5: REFACTOR von PLRS & SNSK (04.11.2026, 17:30)
    def test_very_favorable_rate(self, mock_get):
        _mock_rate(mock_get, 1.25)
        assert get_exchange_rate_assessment("EUR", "USD") == "sehr günstig"


class TestCurrencyServiceApiAufruf:
    # TDD-Zyklus 6: RED von PLRS (04.11.2026, 17:31)
    def test_api_is_called_with_correct_url_and_timeout(self, mock_get):
        _mock_rate(mock_get, 1.05)

        get_exchange_rate_assessment("EUR", "USD")

        mock_get.assert_called_once_with(
            "https://api.exchangerate.com/convert?from=EUR&to=USD",
            timeout=5,
        )


class TestAssessRateGrenzwerte:
    # TDD-Zyklus 7: RED von SNSK (04.11.2026, 17:33)
    # TDD-Zyklus 7: GREEN von PLRS (04.11.2026, 17:35)
    @pytest.mark.parametrize(
        "rate, expected",
        [
            (0.0, "sehr ungünstig"),
            (0.8999, "sehr ungünstig"),
            (0.90, "ungünstig"),
            (0.99, "ungünstig"),
            (0.995, "ungünstig"),
            (1.00, "fair"),
            (1.09, "fair"),
            (1.10, "günstig"),
            (1.19, "günstig"),
            (1.20, "sehr günstig"),
            (2.50, "sehr günstig"),
        ],
    )
    def test_boundaries(self, rate, expected):
        assert assess_rate(rate) == expected


class TestCurrencyServiceDynamischerMock:
    # TDD-Zyklus 8: RED von PLRS (04.11.2026, 17:37)
    def test_different_currency_pairs_with_dynamic_mock(self, mock_get):
        mock_get.side_effect = _fake_currency_api

        assert get_exchange_rate_assessment("EUR", "USD") == "fair"
        assert get_exchange_rate_assessment("EUR", "GBP") == "sehr ungünstig"
        assert get_exchange_rate_assessment("USD", "EUR") == "ungünstig"
        assert get_exchange_rate_assessment("CHF", "EUR") == "günstig"
        assert mock_get.call_count == 4


class TestCurrencyServiceFehlerfaelle:
    # TDD-Zyklus 9: RED von SNSK (04.11.2026, 17:39)
    # TDD-Zyklus 9: GREEN von PLRS (04.11.2026, 17:40)
    def test_missing_rate_raises_value_error(self, mock_get):
        mock_get.return_value.json.return_value = {}

        with pytest.raises(ValueError, match="rate"):
            get_exchange_rate_assessment("EUR", "USD")

    # TDD-Zyklus 10: RED von PLRS (04.11.2026, 17:42)
    # TDD-Zyklus 10: REFACTOR von SNSK & PLRS (04.11.2026, 17:44)
    def test_http_error_is_propagated(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(
            "500 Server Error"
        )

        with pytest.raises(requests.HTTPError):
            get_exchange_rate_assessment("EUR", "USD")
