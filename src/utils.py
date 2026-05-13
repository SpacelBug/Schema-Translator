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