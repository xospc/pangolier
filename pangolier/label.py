from .filters import FilterClause


class Label:
    def __init__(self, name: str):
        self.name = name

    def __eq__(  # type: ignore[override]
        self, expression: str,  # type: ignore[override]
    ) -> FilterClause:
        return FilterClause(self.name, '=', expression)
