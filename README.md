# Pangolier

prometheus query builder

## install

    pip install pangolier

## usage

### simple case

For a metric with filters:

    from pangolier.metrics import Metric

    print(Metric('http_requests_total').filter(
        job='prometheus',
        group='canary'
    ).to_str())

output:

    http_requests_total{job="prometheus", group="canary"}

### pretty output

Add `pretty=True` in `to_str` for better readability:

    from pangolier.metrics import Metric

    print(Metric('http_requests_total').filter(
        job='prometheus',
        group='canary'
    ).to_str(pretty=True))

output:

    http_requests_total{
        job="prometheus",
        group="canary"
    }

I will always use `pretty=True` in rest of this document.

### functions

Prometheus functions can be built by name. For example:

    from pangolier.functions import function

    abs = function('abs')
    print(abs(Metric('http_requests_total')).to_str(pretty=True))

output:

    abs(
        http_requests_total
    )

`range_function` should be used for functions accept a `range-vector`.

    from pangolier.functions import range_function

    rate = range_function('rate')
    print(rate(Metric('http_requests_total'), timespan='5m').to_str(pretty=True))

output:

    rate(
        http_requests_total[5m]
    )

`aggregation_operator` shoule be used for aggregation operators:

    from pangolier.functions import aggregation_operator

    sum_ = aggregation_operator('sum')
    print(sum_(
        Metric('http_requests_total'),
        by=('job', 'group'),
    ).to_str(pretty=True))

output:

    sum by(
        job, group
    )(
        http_requests_total
    )

combine them all together:

    histogram_quantile = function('histogram_quantile')
    rate = range_function('rate')
    sum_ = aggregation_operator('sum')

    print(histogram_quantile(
        0.9,
        sum_(
            rate(
                Metric('http_request_duration_seconds_bucket'),
                timespan='5m',
            ),
            by=('le',)
        )
    ).to_str(pretty=True))

output:

    histogram_quantile(
        0.9,
        sum by(
            le
        )(
            rate(
                http_request_duration_seconds_bucket[5m]
            )
        )
    )

### binary operators

support following binary operators:

* `+` (addition)
* `-` (subtraction)
* `*` (multiplication)
* `/` (division)
* `%` (modulo)
* `^` (power/exponentiation)

For example, divide one metric with another:

    from pangolier.metrics import Metric
    from pangolier.functions import range_function

    rate = range_function('rate')
    print((
        rate(
            Metric('foo').filter(
                group='canary'
            ),
            timespan='5m'
        ) / rate(
            Metric('bar').filter(
                group='canary'
            ),
            timespan='5m'
        )
    ).to_str(pretty=True))

output:

    rate(
        foo{
            group="canary"
        }[5m]
    ) / rate(
        bar{
            group="canary"
        }[5m]
    )

## about name

[Pangolier](https://dota2.fandom.com/wiki/Pangolier)
