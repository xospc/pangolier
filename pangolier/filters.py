class FilterBase:
    def __init__(self, expression):
        self.expression = expression

    def to_str(self, pretty=False):
        raise NotImplementedError


class EqualFilter(FilterBase):
    def to_str(self, pretty=False):
        return '="%s"' % self.expression


class RegexpFilter(FilterBase):
    def to_str(self, pretty=False):
        return '=~"%s"' % self.expression


def _make_filter(value):
    if isinstance(value, str):
        return EqualFilter(value)

    if isinstance(value, FilterBase):
        return value

    raise ValueError('cannot parse filter: %r' % value)
