import json
from typing import Iterator
from unittest import mock


class FuJsonEncoder(json.JSONEncoder):
    """
    JSON Encoder that allows to set the float formatting.
    """

    def __init__(self, *, float_format: str = "f", **kwargs):
        super().__init__(**kwargs)
        self._float = _build_float(float_format)

    def iterencode(self, *args, **kwargs) -> Iterator[str]:
        with mock.patch.object(
            json.encoder, "c_make_encoder", new=None
        ), mock.patch.object(json.encoder, "float", self._float):
            return super().iterencode(*args, **kwargs)


def _build_float(float_format: str = "f") -> type:
    """
    Build class to use as stand-in for `float` builtin type,
    providing custom `float.__repr__()` implementation
    as used in stdlib `json.JSONEncoder.iterencode.floatstr`
    """

    class _Float(float):
        def __repr__(self):
            return format(self, float_format)

    return _Float


def dump(obj, fp, *, float_format: str = "f", **kwargs):
    encoder = FuJsonEncoder(float_format=float_format, **kwargs)
    for chunk in encoder.iterencode(obj):
        fp.write(chunk)


def dumps(obj, *, float_format: str = "f", **kwargs) -> str:
    encoder = FuJsonEncoder(float_format=float_format, **kwargs)
    return encoder.encode(obj)
