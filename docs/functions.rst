functions
=========

Prometheus functions can be built by name. For example:

.. code-block:: python

   from pangolier.functions import function

   abs = function('abs')
   print(abs(
       Metric('http_requests_total')
   ).to_str(pretty=True))

output:

.. code-block::

   abs(
       http_requests_total
   )

``range_function`` should be used for functions accept a ``range-vector``.

.. code-block:: python

   from pangolier.functions import range_function

   rate = range_function('rate')
   print(rate(
       Metric('http_requests_total'),
       timespan='5m'
   ).to_str(pretty=True))

output:

.. code-block::

   rate(
       http_requests_total[5m]
   )

``aggregation_operator`` shoule be used for aggregation operators:

.. code-block:: python

   from pangolier.functions import aggregation_operator

   sum_ = aggregation_operator('sum')
   print(sum_(
       Metric('http_requests_total'),
       by=['job', 'group'],
   ).to_str(pretty=True))

output:

.. code-block::

   sum by(
       job, group
   )(
       http_requests_total
   )

combine them all together:

.. code-block:: python

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
           by=['le']
       )
   ).to_str(pretty=True))

output:

.. code-block::

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
