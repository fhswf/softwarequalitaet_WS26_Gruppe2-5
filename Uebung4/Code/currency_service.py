import requests

API_BASE_URL = "https://api.exchangerate.com/convert"
TIMEOUT_SECONDS = 5

_ASSESSMENT_THRESHOLDS = [
    (0.90, "sehr ungünstig"),
    (1.00, "ungünstig"),
    (1.10, "fair"),
    (1.20, "günstig"),
]
_HIGHEST_ASSESSMENT = "sehr günstig"


def build_url(from_currency: str, to_currency: str) -> str:
    return f"{API_BASE_URL}?from={from_currency}&to={to_currency}"


def fetch_exchange_rate(from_currency: str, to_currency: str) -> float:
    response = requests.get(build_url(from_currency, to_currency), timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()

    rate = data.get("rate")
    if rate is None:
        raise ValueError(
            f"API-Antwort enthält keinen Wechselkurs ('rate') für {from_currency}->{to_currency}"
        )
    return float(rate)


def assess_rate(rate: float) -> str:
    for upper_bound, assessment in _ASSESSMENT_THRESHOLDS:
        if rate < upper_bound:
            return assessment
    return _HIGHEST_ASSESSMENT


def get_exchange_rate_assessment(from_currency: str, to_currency: str) -> str:
    rate = fetch_exchange_rate(from_currency, to_currency)
    return assess_rate(rate)
