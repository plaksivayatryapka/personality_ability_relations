def clean(string: str) -> str:
    string = string.lstrip()
    string = string.replace('cd.-', '')
    return string