.. include:: global.rst.inc
.. highlight:: console
.. _perftips:

Performance tips
================

Here are some tips which can help to improve performance of ZenMake in some cases.

Hash algorithm
"""""""""""""""""""""
By default ZenMake uses sha1 algorithm to control changes of config/built files
and for some other things. Modern CPUs often have support
for this algorithm and sha1 shows better or almost the same
performance as md5 in this cases. But in some other cases md5 can be
faster and you can switch to use this hash algorithm. However, don't expect a big
difference in performance of ZenMake.

It's recommended to check if it really has positive effect before using of md5.
To change hash algorithm you can use parameter ``hash-algo`` in buildconf
:ref:`general features<buildconf-general>`.
