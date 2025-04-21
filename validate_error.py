#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class ValidateError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(value)


class OneOfError(ValidateError):
    def __init__(self, value, options):
        self.options = options
        super().__init__(value)

    def __str__(self):
        return f"Expected {self.value!r} to be one of {self.options}"


class NumberError(ValidateError):
    def __init__(self, value, minvalue=None, maxvalue=None):
        super().__init__(value)
        self.minvalue = minvalue
        self.maxvalue = maxvalue


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
    pass


class StringShortError(StringError):
    pass


class StringLongError(StringError):
    pass


class StringPredicateError(StringError):
    pass
