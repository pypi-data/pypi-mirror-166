# `shortfun`

This package provides a functional way to use python operators. Using this package would prevent the need to do something such as:

```py
lambda x: x + 10
```

where we use a lambda function to pass in arguments to a function (in this case +) one at a time.

## Examples:

```py
>>> from shortfun import sf

>>> filtered = filter(sf.gt(10), [1, 20, 10, 8, 30])  # Greater-than function
>>> list(filtered)
[20, 30]
```

```py
>>> from shortfun import sf

>>> mapped = map(sf.add(10), [1, 20, 10, 8, 30])  # Addition function
>>> list(mapped)
[11, 30, 20, 18, 40]
```

The majority of python dunder methods are implemented in `shortfun` where it makes sense.

## Even Shorter Functions

This API is more limited, but in certain situations you can use the underscore variable provided by this package as a replacement for `lambda x: x ...`

```py
>>> from shortfun import _

>>> filtered = filter(_ > 10, [1, 20, 10, 8, 30])  # instead of: lambda x: x > 10
>>> list(filtered)
[20, 30]
```

```py
>>> from shortfun import _

>>> mapped = map(_ + 10, [1, 20, 10, 8, 30]) # instead of: lambda x: x + 10
>>> list(mapped)
[11, 30, 20, 18, 40]
```
