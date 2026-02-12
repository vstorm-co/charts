from charts.base_types import BaseTable, BaseTableData, BaseTableFooter


class TableData(BaseTableData):
    """Collection of data to present in the table.

    Exemplary format:
    headers = ["month", "price", "id", ...]
    rows = [
        ("september", "19.99", "asd21331", ...),
        ("may", "109.99", "d2134sdf", ...),
        ...
    ]
    """


class TableFooter(BaseTableFooter):
    """A footer of the table."""


class Table(BaseTable):
    """A Table component."""

    component_type: str = "table"
