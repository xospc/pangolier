binary operators
================

support following binary operators:

* ``+`` (addition)
* ``-`` (subtraction)
* ``*`` (multiplication)
* ``/`` (division)
* ``%`` (modulo)
* ``^`` (power/exponentiation)

For example, divide one metric with another:

.. code-block:: python

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

.. code-block::

   rate(
       foo{
           group="canary"
       }[5m]
   ) / rate(
       bar{
           group="canary"
       }[5m]
   )

For operation with modifier:

.. code-block:: python

   from pangolier.metrics import Metric, BinOp, GroupLeft

   print(BinOp(
       '*',
       Metric('foo'),
       Metric('bar'),
       on=['interface', 'job'],
       group=GroupLeft('node', 'resource'),
   ).to_str(pretty=True))

output:

.. code-block::

   foo * on(
       interface, job
   ) group_left(
       node, resource
   ) bar
