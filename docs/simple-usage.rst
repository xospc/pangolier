simple usage
============

basic
-----

For a metric with filters:

.. code-block:: python

   from pangolier.metrics import Metric

   print(Metric('http_requests_total').filter(
       job='prometheus',
       group='canary'
   ).to_str())

output:

.. code-block::

   http_requests_total{job="prometheus", group="canary"}

pretty output
-------------

Add ``pretty=True`` in ``to_str`` for better readability:

.. code-block:: python

   from pangolier.metrics import Metric

   print(Metric('http_requests_total').filter(
       job='prometheus',
       group='canary'
   ).to_str(pretty=True))

output:

.. code-block::

   http_requests_total{
       job="prometheus",
       group="canary"
   }

I will always use ``pretty=True`` in rest of this document.
