from typing import Optional
from collections.abc import Callable

from pangolier.metrics import MetricBase
from pangolier.bin_op import BinOp, GroupBase


def make_multiply_func(
    on: Optional[list[str]] = None,
    group: Optional[GroupBase] = None,
    reverse: bool = False,
) -> Callable[[MetricBase, MetricBase], MetricBase]:
    def multiply(first: MetricBase, second: MetricBase) -> MetricBase:
        if reverse:
            return BinOp(
                '*', second, first, on=on, group=group
            )

        return BinOp(
            '*', first, second, on=on, group=group
        )

    return multiply
