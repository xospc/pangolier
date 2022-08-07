# Pangolier

prometheus query builder

## install

    pip install pangolier

## usage

### simple case:

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

You can disable it as you like.

### functions

Pangolier supports some prometheus functions, like `sum`, `rate` and `histogram_quantile`.

    from pangolier.metrics import Metric
    from pangolier.functions import Rate, Sum, HistogramQuantile

    print(Rate(Metric('http_requests_total'), timespan='5m').to_str(pretty=True))
    print(Sum(Metric('http_requests_total'), by=('job', 'group')).to_str(pretty=True))
    print(HistogramQuantile(
        0.9,
        Sum(
            Rate(
                Metric('http_request_duration_seconds_bucket'),
                timespan='5m',
            ),
            by=('le',)
        )
    ).to_str(pretty=True))

output:

    rate(
        http_requests_total[5m]
    )
    sum by(
        job, group
    )(
        rate(
            http_requests_total[5m]
        )
    )
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

More functions will be added in future.

### bin op

divide one metric with another:

    from pangolier.metrics import Metric
    from pangolier.functions import Rate

    print((
        Rate(
            Metric('foo').filter(
                group='canary'
            ),
            timespan='5m'
        ) / Rate(
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

More operations will be added in future.

## about name

[Pangolier](https://dota2.fandom.com/wiki/Pangolier)
