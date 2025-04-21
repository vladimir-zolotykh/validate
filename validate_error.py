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
    pass


class NumberLowErrror(NumberError):
    pass


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
