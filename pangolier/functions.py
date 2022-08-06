from .common import indent_body


class FunctionBase:
    def to_str(self, pretty=False):
        raise NotImplementedError


class Rate(FunctionBase):
    # Should I give timespan a default value.
    # Maybe 5m?
    def __init__(self, origin_metric, timespan):
        self.origin_metric = origin_metric
        self.timespan = timespan

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if pretty:
            return 'rate(\n%s[%s]\n)' % (
                indent_body(body),
                self.timespan
            )

        return 'rate(%s[%s])' % (body, self.timespan)


class Sum(FunctionBase):
    def __init__(self, origin_metric, by=None):
        self.origin_metric = origin_metric
        self.by = by

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if self.by:
            by_str = ', '.join(self.by)

            if pretty:
                return 'sum by(\n%s\n)(\n%s\n)' % (
                    indent_body(by_str),
                    indent_body(body)
                )
            return 'sum by(%s)(%s)' % (
                by_str,
                body
            )

        if pretty:
            return 'sum(\n%s\n)' % (
                indent_body(body),
            )

        return 'sum(%s)' % body
