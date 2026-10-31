# Implementiert von: MXMR, CNStS
"""
FizzBuzz-Kata (Team A, Übung 4) – testgetrieben entwickelt.

FizzBuzz-Regeln:
- Zahl durch 3 teilbar -> "Fizz"
- Zahl durch 5 teilbar -> "Buzz"
- Zahl durch 3 UND 5 teilbar -> "FizzBuzz"
- Sonst -> Zahl als String
"""


def fizzbuzz(n: int) -> str:
    """
    Wandelt eine positive Ganzzahl nach den FizzBuzz-Regeln in einen String um.

    Args:
        n: Eine positive Ganzzahl

    Returns:
        "Fizz", "Buzz", "FizzBuzz" oder die Zahl als String

    Raises:
        TypeError: n ist kein int (auch bool wird abgelehnt)
        ValueError: n ist kleiner als 1
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n muss int sein, war {type(n).__name__}")
    if n < 1:
        raise ValueError(f"n muss positiv sein, war {n}")

    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
