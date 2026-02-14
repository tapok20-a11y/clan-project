from datetime import datetime


def valid_name(name: str) -> bool:
    cleaned = name.strip()
    return len(cleaned) >= 2 and any(ch.isalpha() for ch in cleaned)


def valid_age(age: str) -> bool:
    return age.isdigit() and 0 < int(age) < 120


def valid_nonempty(text: str, min_len: int = 2) -> bool:
    return len(text.strip()) >= min_len


def valid_birth_date(text: str) -> bool:
    value = text.strip()
    for fmt in ("%d.%m", "%d/%m", "%d-%m"):
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False
