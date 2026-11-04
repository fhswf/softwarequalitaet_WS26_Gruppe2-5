import re

DEFAULT_DELIMITER = ","
CUSTOM_DELIMITER_PREFIX = "//"
MAX_VALUE = 1000


def _parse_delimiter(numbers: str) -> tuple[str, str]:
    if numbers.startswith(CUSTOM_DELIMITER_PREFIX):
        header, _, body = numbers.partition("\n")
        return header[len(CUSTOM_DELIMITER_PREFIX):], body
    return DEFAULT_DELIMITER, numbers


def _split(body: str, delimiter: str) -> list[str]:
    pattern = f"{re.escape(delimiter)}|\n"
    return [part for part in re.split(pattern, body) if part != ""]


def _parse_numbers(numbers: str) -> list[int]:
    delimiter, body = _parse_delimiter(numbers)
    return [int(part) for part in _split(body, delimiter)]


def _validate_no_negatives(values: list[int]) -> None:
    negatives = [n for n in values if n < 0]
    if negatives:
        raise ValueError(
            "negatives not allowed: " + ", ".join(str(n) for n in negatives)
        )


def _ignore_too_large(values: list[int]) -> list[int]:
    return [n for n in values if n <= MAX_VALUE]


def add(numbers: str) -> int:
    if numbers == "":
        return 0

    values = _parse_numbers(numbers)
    _validate_no_negatives(values)
    return sum(_ignore_too_large(values))
