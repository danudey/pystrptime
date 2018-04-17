# pystrptime

A really, really dumb `strptime` "implementation" for Python.

### What doesn't it do?

Basically it takes a format like `2012-02-02 12:23:49` and
turns it into `datetime.datetime(2012, 2, 2, 12, 23, 49)`.
There's no timezones, no daylight savings, no anything. Just
go from a string to a datetime that matches the numbers in
that string or raise a ValueError if it doesn't.

### Stupid benchmarks

For a list of 256,806 matching strings:

    In [3]: %%timeit
       ...: for line in dates:
       ...:     dt = datetime.datetime.strptime(line, form)
       ...:
    1 loop, best of 3: 4.43 s per loop

    In [2]: %%timeit
       ...: for line in dates:
       ...:     dt = strptime.strptime(line, form)
       ...:
    10 loops, best of 3: 95.8 ms per loop

This is a 47x improvement over the `datetime` module itself.
