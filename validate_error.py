#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class ValidateError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(value)


class OneOfError(ValidateError):
    pass


class NumberError(ValidateError):
    pass


class NumberTypeError(NumberError):
    def __str__(self):
        return f"Expected {self.value!r} of type int or float"


class NumberLowError(NumberError):
    def __init__(self, value, minvalue):
        super().__init__(value)
        self.minvalue = minvalue

    def __str__(self):
        return f"Expected {self.value!r} >= {self.minvalue}"


class NuberHighError(NumberError):
    pass


class StringError(ValidateError):
    pass


class StringShortError(StringError):
    pass


class StringLongError(StringError):
    pass


class StringPredicateError(StringError):
    pass
