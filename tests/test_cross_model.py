from src.translator import Column, CrossColumn, CrossModel

def test_column_class():
    column = Column(name="test_column", type="string")
    assert column.name == "test_column"
    assert column.type == "string"


def test_cross_column_class():
    old_column = Column(name="old_value", type="string")
    new_column = Column(name="new_value", type="string")

    cross_column = CrossColumn(old_column=old_column, new_column=new_column)

    assert cross_column.old_column == old_column
    assert cross_column.new_column == new_column


def test_cross_model_class():
    old_column = Column(name="old_value", type="string")
    new_column = Column(name="new_value", type="string")

    cross_column = CrossColumn(old_column=old_column, new_column=new_column)

    cross_model = CrossModel(name="test_cross_model", columns=[cross_column])

    assert cross_model.name == "test_cross_model"
    assert cross_model.columns == [cross_column]


def test_cross_model_from_dict():
    cross_model = CrossModel.from_dict(
        "test_cross_model",
        [
            {
                "old_column": {"name": "old_id", "type": "string"},
                "new_column": {"name": "new_id", "type": "integer"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_date", "type": "string"},
                "new_column": {"name": "new_date", "type": "date"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_value", "type": "string"},
                "new_column": {"name": "new_value", "type": "float"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_datetime", "type": "string"},
                "new_column": {"name": "new_datetime", "type": "datetime"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_datetime", "type": "string"},
                "new_column": {"name": "new_datetime", "type": "boolean"},
                "mapping": None,
            },
            {
                "old_column": {
                    "name": ["old_extra_date", "old_extra_time"],
                    "type": "string",
                },
                "new_column": {"name": "new_extra_datetime", "type": "datetime"},
                "mapping": None,
            },
        ],
    )

    assert cross_model.name == "test_cross_model"

    assert len(cross_model.columns) == 6

    assert cross_model.columns[0].old_column.name == "old_id"
    assert cross_model.columns[0].old_column.type == "string"
    assert cross_model.columns[0].new_column.name == "new_id"
    assert cross_model.columns[0].new_column.type == "integer"

    assert cross_model.columns[1].old_column.name == "old_date"
    assert cross_model.columns[1].old_column.type == "string"
    assert cross_model.columns[1].new_column.name == "new_date"
    assert cross_model.columns[1].new_column.type == "date"

    assert cross_model.columns[2].old_column.name == "old_value"
    assert cross_model.columns[2].old_column.type == "string"
    assert cross_model.columns[2].new_column.name == "new_value"
    assert cross_model.columns[2].new_column.type == "float"

    assert cross_model.columns[3].old_column.name == "old_datetime"
    assert cross_model.columns[3].old_column.type == "string"
    assert cross_model.columns[3].new_column.name == "new_datetime"
    assert cross_model.columns[3].new_column.type == "datetime"

    assert cross_model.columns[4].old_column.name == "old_datetime"
    assert cross_model.columns[4].old_column.type == "string"
    assert cross_model.columns[4].new_column.name == "new_datetime"
    assert cross_model.columns[4].new_column.type == "boolean"

    assert cross_model.columns[5].old_column.name == [
        "old_extra_date",
        "old_extra_time",
    ]
    assert cross_model.columns[5].old_column.type == "string"
    assert cross_model.columns[5].new_column.name == "new_extra_datetime"
    assert cross_model.columns[5].new_column.type == "datetime"


def test_cross_model_transform_to_new():
    cross_model = CrossModel.from_dict(
        "test_cross_model",
        [
            {
                "old_column": {"name": "old_id", "type": "string"},
                "new_column": {"name": "new_id", "type": "integer"},
                "mapping": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5},
            },
            {
                "old_column": {"name": "old_date", "type": "string"},
                "new_column": {"name": "new_date", "type": "date"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_value", "type": "string"},
                "new_column": {"name": "new_value", "type": "float"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_datetime", "type": "string"},
                "new_column": {"name": "new_datetime", "type": "datetime"},
                "mapping": None,
            },
            {
                "old_column": {"name": "old_datetime", "type": "string"},
                "new_column": {"name": "new_datetime", "type": "boolean"},
                "mapping": None,
            },
            {
                "old_column": {
                    "name": ["old_extra_date", "old_extra_time"],
                    "type": "string",
                },
                "new_column": {"name": "new_extra_datetime", "type": "datetime"},
                "mapping": None,
            },
        ],
    )

    data = [
        {
            "old_id": "one",
            "old_date": "2023-01-01",
            "old_value": "10.5",
            "old_datetime": "2023-01-01 12:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "two",
            "old_date": "2023-01-02",
            "old_value": "20.5",
            "old_datetime": "2023-01-02 13:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "three",
            "old_date": "2023-01-03",
            "old_value": "11.2",
            "old_datetime": "2023-01-02 14:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "four",
            "old_date": "2023-01-04",
            "old_value": "23.5",
            "old_datetime": "2023-01-02 15:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "five",
            "old_date": "2023-01-05",
            "old_value": "25.5",
            "old_datetime": "2023-01-02 23:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "6",
            "old_date": "2023-01-05",
            "old_value": "25.5",
            "old_datetime": "2023-01-02 23:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
        {
            "old_id": "6",
            "old_date": "2023-01-05",
            "old_value": "25.5",
            "old_datetime": "2023-01-02 23:00:00",
            "old_extra_date": "2023-01-02",
            "old_extra_time": "23:00:00",
        },
    ]

    transformed_data = cross_model.transform_to_new(data, True)

    print(transformed_data)
