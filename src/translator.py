import inspect

from dateutil.parser import ParserError

from .exceptions import CrossModelExceptions
from .utils import check_values_in_row

class Column:
    def __init__(
        self,
        name: str | list,
        type: str,
    ):
        if type not in ["string", "integer", "float", "boolean", "date", "datetime"]:
            raise CrossModelExceptions("TypeError", f"Type {type} is not supported")

        self.name = name
        self.type = type


class CrossColumn:
    """Class, which describe of columns in old and new models.

    Attributes:
        new_column: Column object, which describe column in new model
        old_column: Column object, which describe column in old model
        mapping: dict, which describe mapping of column values.

    Methods:
        map: method, which map value from old model to new model using mapping dict.
        parse_types: method, which parse value to new type using type from new column.
    """

    def __init__(
        self,
        new_column: Column,
        old_column: Column,
        mapping: dict = None,
        values_to_column: list[dict] = None,
    ):
        """Constructor of CrossColumn class.

        Parameters:
            new_column: Column object, which describe column in new model
            old_column: Column object, which describe column in old model
            mapping: dict, which describe mapping of column values.
            values_to_column: list of values, which should be transformed to new column.
        """
        self.new_column = new_column
        self.old_column = old_column

        self.mapping = mapping
        """Describe mapping of column values. 
        
        Key is a value in new model, value is a value in old model, which should be transformed to new model value.
        For example, if we have column "status" in new model, which can have values "active", "inactive", "pending", and in old model we have column 
        "status_code", which can have values 1, 0, 2, and these values are mapping (1 -> active, 0 -> inactive, 2 -> pending), then mapping should be:
        
        ```
        mapping = { "1": 4, "2": 2, "3": 1 }
        ```
        """

        self.values_to_column = values_to_column
        """Describe list of values, which should be transformed to new column.
        ```
        values_to_column = [
            {"value": "e4rds321sd1", "column": Column(name="new_public_id", type="string")},
            {"value": "ksi388sd3fu", "column": Column(name="new_public_id", type="string"), "new_value": "test_value"},
        ]
        ```
        """

    def map(self, value, missed_values=False):
        """Map value from old model to new model using mapping dict.

        Parameters:
            value: value which should be transformed
            missed_values: if True, then if value is not found in mapping, it will be returned as is, otherwise None will be returned
        """
        if self.mapping is not None:
            return self.mapping.get(value, value if missed_values else None)

    def parse_types(self, value):
        """Parse value to new type using type from new column.

        date format should be "YYYY-MM-DD", datetime format should be "YYYY-MM-DD HH:MM:SS"

        Parameters:
            value: value which should be parsed
        """
        if self.new_column.type is not None:
            if self.new_column.type == "string":
                return str(value)
            elif self.new_column.type == "integer":
                return int(value)
            elif self.new_column.type == "float":
                return float(value)
            elif self.new_column.type == "boolean":
                return bool(value)
            elif self.new_column.type == "date":
                from datetime import datetime

                return datetime.strptime(value, "%Y-%m-%d").date()
            elif self.new_column.type == "datetime":
                from dateutil.parser import parser

                return parser().parse(value, ignoretz=True, yearfirst=True)


class CrossModel:
    """
    Class, which describe cross model.

    Attributes:
        name: name of cross model
        columns: list of `CrossColumn` objects, which describe columns in old and new models.
    """

    def __init__(self, name: str, columns: list[CrossColumn]):
        """Constructor of CrossModel class.

        Parameters:
            name: name of cross model
            columns: list of `CrossColumn` objects, which describe columns in old and new models.
        """
        self.name = name
        self.columns = columns

    def transform_to_new(
        self,
        old_data: list[dict],
        map_missed_values: bool = False,
        mode: str | None = "strict",
    ) -> list[dict]:
        """Transform data from old model to new model using columns description in self.columns.

        Parameters:
            old_data:
                list of dict, which describe data in old model.

            map_missed_values:
                if True, then if value is not found in mapping, it will be returned as is, otherwise None will be returned.

            mode:
                ['strict', 'lenient', 'exclusive', 'perverse']
                If 'strict' (default value), then if column is not found in old data or can`t be parsed, CrossColumnError will be raised, if 'lenient',
                then column will be skipped, 'perverse', then column will be added to new data when it is broken.

        Returns:
            list of dict, which describe data in new model
        """

        new_data = []

        for row in old_data:
            skip_row = False
            new_row = {}

            for cross_column in self.columns:
                if check_values_in_row(cross_column.old_column.name, row):
                    # TODO: add column splitting
                    # get value from old data using old column name, if old column name is a string, otherwise get concatenated value from old data using old column names
                    value = (
                        row[cross_column.old_column.name]
                        if isinstance(cross_column.old_column.name, str)
                        else " ".join(
                            [
                                str(row[column_name])
                                for column_name in cross_column.old_column.name
                            ]
                        )
                    )

                    if cross_column.values_to_column is not None:
                        value_found = False
                        for new_values in cross_column.values_to_column:
                            search_value = new_values.get("value")
                            if value == search_value:
                                column = new_values.get("column")
                                new_value = new_values.get("new_value", value)
                                new_row[column.name] = new_value
                                value_found = True
                                break
                        if value_found:
                            continue
                    else:
                        # if mapping is not None, then map value, otherwise return value as is
                        if cross_column.mapping is not None:
                            value = cross_column.map(
                                value, missed_values=map_missed_values
                            )
                        # if types are different, then parse value to new type, otherwise return value as is
                        if (
                            cross_column.new_column.type != cross_column.old_column.type
                        ) and (value is not None):
                            try:
                                value = cross_column.parse_types(value)
                            except ParserError:
                                if mode == "lenient":
                                    print(f"Row with broken value: {value} \n {row}")
                                    skip_row = True
                                    break
                                else: 
                                    raise ParserError
                            except ValueError:
                                if mode == "lenient":
                                    print(f"Row with broken value: {value} \n {row}")
                                    skip_row = True
                                    break
                                else:
                                    raise ValueError
                    new_row[cross_column.new_column.name] = value
                else:
                    if mode == "strict":
                        raise CrossModelExceptions(
                            "CrossColumnError",
                            f"Column {cross_column.old_column.name} not found in old data",
                        )
                    elif mode == "lenient":
                        skip_row = True
                        break
            
            if skip_row:
                continue
            else:
                new_data.append(new_row)

        return new_data

    def transform_to_old(self, new_data: list[dict]) -> list[dict]:
        # TODO: implement transform_to_old method
        pass

    @staticmethod
    def from_dict(name: str, schema: dict):
        """Create `CrossModel` instance from dictionary.

        Parameters:
            name: name of cross model
            data: dict, which describe cross model. Should have the following structure:
            ```
            [
                {
                    new_column: {"name": "status", "type": "string"},
                    old_column: {"name": "status_code", "type": "integer"},
                    mapping: {"1": "active", "0": "inactive", "2": "pending"},
                    values_to_column: [
                        {"value": "e4rds321sd1", "column": Column(name="new_public_id", type="string")},
                        {"value": "ksi388sd3fu", "column": Column(name="new_public_id", type="string"), "new_value": "test_value"},
                    ]
                },
            ]
            ```

        Returns:
            `CrossModel` instance
        """

        cross_model = CrossModel(name=name, columns=[])

        for cross_column in schema:
            if "new_column" not in cross_column or "old_column" not in cross_column:
                raise CrossModelExceptions(
                    "CrossModelError",
                    f"Each column should have 'new_column' and 'old_column' keys",
                )

            new_column = cross_column["new_column"]
            old_column = cross_column["old_column"]
            mapping = cross_column.get("mapping")
            values_to_column = cross_column.get("values_to_column")

            if "name" not in new_column or "type" not in new_column:
                raise CrossModelExceptions(
                    "CrossModelError",
                    "New column should have 'name' and 'type' keys",
                )
            if "name" not in old_column or "type" not in old_column:
                raise CrossModelExceptions(
                    "CrossModelError",
                    "Old column should have 'name' and 'type' keys",
                )

            new_column_obj = Column(name=new_column["name"], type=new_column["type"])
            old_column_obj = Column(name=old_column["name"], type=old_column["type"])

            cross_column = CrossColumn(
                new_column=new_column_obj,
                old_column=old_column_obj,
                mapping=mapping,
                values_to_column=values_to_column,
            )
            cross_model.columns.append(cross_column)

        return cross_model
