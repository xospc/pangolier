Pangolier
=========

build PromQL by Python code.

install
-------

.. code-block::

    pip install pangolier

simple usage
------------

basic
~~~~~

For a metric with filters:

.. code-block:: python

   from pangolier.metrics import Metric

   print(Metric('http_requests_total').filter(
       job='prometheus',
       group='canary'
   ).to_str())

or with label style and method `where`:

.. code-block:: python

   from pangolier.metrics import Metric
   from pangolier.label import Label

   print(Metric('http_requests_total').where(
        Label('job') == 'prometheus',
        Label('group') == 'canary',
   ).to_str())

output:

.. code-block::

   http_requests_total{job="prometheus", group="canary"}

pretty output
~~~~~~~~~~~~~

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

read more:

.. toctree::
  :maxdepth: 1

  functions
  bin-op
  about
