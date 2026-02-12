def valid_name(name: str) -> bool:
    return len(name.strip()) >= 2

def valid_age(age: str) -> bool:
    if not age.isdigit():
        return False
    return int(age) <= 11

def valid_nonempty(text: str) -> bool:
    return len(text.strip()) > 0
