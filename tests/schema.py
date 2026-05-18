from src.translator import Column

schema = [
    {
        "old_column": {"name": "old_id", "type": "string"},
        "new_column": {"name": "new_id", "type": "integer"},
        "mapping": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5},
        "values_to_column": [
            {"value": "e4rds321sd1", "column": Column(name="new_public_id", type="string")},
            {"value": "ksi388sd3fu", "column": Column(name="new_public_id", type="string"), "new_value": "test_value"},
        ],
    },
    {
        "old_column": {"name": "old_date", "type": "string"},
        "new_column": {"name": "new_date", "type": "date"},
    },
    {
        "old_column": {"name": "old_value", "type": "string"},
        "new_column": {"name": "new_value", "type": "float"},
    },
    {
        "old_column": {"name": "old_datetime", "type": "string"},
        "new_column": {"name": "new_datetime", "type": "datetime"},
    },
    {
        "old_column": {"name": "old_datetime", "type": "string"},
        "new_column": {"name": "new_datetime", "type": "boolean"},
    },
    {
        "old_column": {
            "name": ["old_extra_date", "old_extra_time"],
            "type": "string",
        },
        "new_column": {"name": "new_extra_datetime", "type": "datetime"},
    },
]
