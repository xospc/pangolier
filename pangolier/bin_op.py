from typing import Optional
from functools import cache

from .metrics import MetricBase

from .common import bracket, format_modifier

OPERATOR_PRECEDENCE = [
    ['^'],
    ['*', '/', '%', 'atan2'],
    ['+', '-'],
    ['==', '!=', '<=', '<', '>=', '>'],
    ['and', 'unless'],
    ['or'],
]
RIGHT_ASSOCIATIVE_OPERATORS = ['^']


@cache
def get_precedence_map() -> dict[str, int]:
    length = len(OPERATOR_PRECEDENCE)

    r: dict[str, int] = {}
    for row, items in enumerate(OPERATOR_PRECEDENCE):
        precedence = length - row
        for op in items:
            r[op] = precedence

    return r


def get_precedence(operator: str) -> int:
    m = get_precedence_map()
    return m[operator]


def need_bracket_for_precedence(metric: MetricBase, parent_op: str) -> bool:
    return (
        isinstance(metric, BinOp)
        and get_precedence(parent_op) > get_precedence(metric.op)
    )


class GroupBase:
    modifier = ''
    labels: list[str]

    def __init__(self, *labels: str):
        self.labels = list(labels)

    def to_str(self, force_bracket: bool = False, pretty: bool = False) -> str:
        return format_modifier(
            self.modifier, self.labels,
            force_bracket=force_bracket, pretty=pretty,
        )


class GroupLeft(GroupBase):
    modifier = 'group_left'


class GroupRight(GroupBase):
    modifier = 'group_right'


class BinOp(MetricBase):
    op: str
    first: MetricBase
    second: MetricBase

    on: Optional[list[str]]
    ignoring: Optional[list[str]]
    group: Optional[GroupBase]

    def __init__(
        self,
        op: str,
        first: MetricBase,
        second: MetricBase,
        *,
        on: Optional[list[str]] = None,
        ignoring: Optional[list[str]] = None,
        group: Optional[GroupBase] = None,
    ):
        if on and ignoring:
            raise ValueError('can not specific both `on` and `ignoring`')

        self.op = op
        self.first = first
        self.second = second

        self.on = on
        self.ignoring = ignoring
        self.group = group

    def to_str(self, pretty: bool = False) -> str:
        parts = []

        first_str = self.first.to_str(pretty=pretty)
        if need_bracket_for_precedence(self.first, self.op):
            first_str = bracket(first_str, pretty=pretty)

        parts.append(first_str)
        parts.append(self.op)

        if self.on:
            parts.append(
                format_modifier('on', self.on, pretty=pretty)
            )

        if self.ignoring:
            parts.append(
                format_modifier('ignoring', self.ignoring, pretty=pretty)
            )

        second_str = self.second.to_str(pretty=pretty)
        if need_bracket_for_precedence(self.second, self.op):
            second_str = bracket(second_str, pretty=pretty)

        if self.group:
            group_need_bracket = second_str.startswith('(')
            parts.append(self.group.to_str(
                force_bracket=group_need_bracket, pretty=pretty
            ))

        parts.append(second_str)

        return ' '.join(parts)
