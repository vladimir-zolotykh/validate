#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(
                f'Expected {value!r} to be one of {self.options!r}')


class Number(Validator):
    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} is int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f'Expected {value!r} is >= than {self.minvalue}')
        if self.maxvalue is not None and self.maxvalue < value:
            raise ValueError(f'Expected {value!r} <= than {self.maxvalue!r}')


class String(Validator):
    def __init__(self, minsize, maxsize, predicate):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} is of type str')
        if len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} is not shorter than {self.minsize!r}')
        if self.maxsize < len(value):
            raise ValueError(
                f'Expected {value!r} is not longer than {self.maxsize!r}')
        if not self.predicate(value):
            raise ValueError(
                f'Expected {value!r} is {self.predicate.__name__}')


class Component:
    name = String(3, 9, str.isupper)
    kind = OneOf('wood', 'metal', 'plastic')
    quantity = Number(minvalue=0, maxvalue=50)

    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity


if __name__ == '__main__':
    Component('a', 'wood', 10)
