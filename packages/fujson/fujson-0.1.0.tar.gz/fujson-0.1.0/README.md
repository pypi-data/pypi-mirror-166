
# FuJSON: less decimals, more fuzzy JSON

FuJSON is a Python module that allows to control the 
formatting of floats when JSON encoding, 
typically to dial down the number of decimals.

It builds on the *standard library*'s `json.JSONEncoder`
and *monkey-patches* it to inject custom float formatting.


## Usage

Simple `dumps` call:

    >>> from fujson import dumps
    >>> dumps({"x": 1.23456789}, float_format=".2f")
    '{"x": 1.23}'

Reusable encoder:

    >>> from fujson import FuJsonEncoder
    >>> encoder = FuJsonEncoder(float_format=".2f")
    >>> encoder.encode({"x": 1.23456789})
    '{"x": 1.23}'
    >>> encoder.encode([1.1, 2.22, 3.333, 4.4444])
    '[1.10, 2.22, 3.33, 4.44]'

Do JSON dump with floats in scientific notation:

    >>> from fujson import FuJsonEncoder
    >>> encoder = FuJsonEncoder(float_format=".2e")
    >>> encoder.encode([.123, 0.0000123, 12345678.9])
    '[1.23e-01, 1.23e-05, 1.23e+07]'


