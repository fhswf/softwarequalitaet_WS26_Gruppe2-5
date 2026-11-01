import requests


def get_weather_category(city: str) -> str:
    """
    Ruft Weather-API auf und gibt Temperatur-Kategorie zurück
    
    Args:
        city: Stadt, für die das Wetter abgefragt wird
        
    Returns:
        Temperatur-Kategorie als String:
        - "frostgefahr" (< 0°C)
        - "kalt" (0-10°C)
        - "kühl" (11-15°C)
        - "angenehm" (16-24°C)
        - "warm" (25-30°C)
        - "heiß" (> 30°C)
    """
    url = f"https://api.weather.com/current?city={city}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    temperature = response.json()["temperature"]

    if temperature < 0:
        return "frostgefahr"
    if temperature <= 10:
        return "kalt"
    if temperature <= 15:
        return "kühl"
    if temperature <= 24:
        return "angenehm"
    if temperature <= 30:
        return "warm"
    return "heiß"
