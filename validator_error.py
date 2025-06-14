#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import validator_data as VD


class ValidateError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(value)

    def __getattr__(self, name):
        if name in self.delegated_fields:
            return getattr(self.data, name)
        # fmt: off
        raise AttributeError(
            f"{type(self).__name__!r} has no attribute {name!r}")
        # fmt: on


class OneOfError(ValidateError):
    def __init__(self, value, data: VD.OneOf0):
        self.options = data.options
        super().__init__(value)

    def __str__(self):
        return f"Expected {self.value!r} to be one of {self.options}"


class NumberError(ValidateError):
    delegated_fields = ("minvalue", "maxvalue")

    def __init__(self, value, data: VD.Number0):
        super().__init__(value)
        self.data = data


class NumberTypeError(NumberError):
    def __str__(self):
        return f"Expected {self.value!r} of type int or float"


class NumberLowError(NumberError):
    def __str__(self):
        return f"Expected {self.value!r} >= {self.minvalue}"


class NumberHighError(NumberError):
    def __str__(self):
        return f"Expected {self.value!r} <= {self.maxvalue}"


class StringError(ValidateError):
    delegated_fields = ("minsize", "maxsize", "predicate")

    def __init__(self, value, data: VD.String0):
        super().__init__(value)
        self.data = data


class StringShortError(StringError):
    def __str__(self):
        return f"Expected len({self.value!r}) >= {self.minsize}"


class StringLongError(StringError):
    def __str__(self):
        return f"Expected len({self.value!r}) <= {self.maxsize}"


class StringPredicateError(StringError):
    def __str__(self):
        return f"Expected {self.predicate.__name__}({self.value!r}) is true"
