def check_values_in_row(values: str | list, row: dict):
    if not values:
        return False
    if isinstance(values, str):
        return values in row
    elif isinstance(values, list):
        for value in values:
            if not value in row:
                return False
        return True
    
def parse_boolean(value: str) -> bool:
    if value.lower() in ["true", "1", "yes"]:
        return True
    elif value.lower() in ["false", "0", "no"]:
        return False
    else:
        raise ValueError(f"Cannot parse boolean value from '{value}'")
