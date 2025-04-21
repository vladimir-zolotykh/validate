#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import unittest
import validate_error as VE


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
        setattr(self, self.private_name, name)

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise VE.OneOfError(value)


class Number(Validator):
    def __init__(self, minvalue=0, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise VE.NumberTypeError(value)
        if value < self.minvalue:
            # raise ValueError(f"Expected {value!r} >= {self.minvalue}")
            raise VE.NumberLowError(value, self.minvalue)
        if self.maxvalue < value:
            # raise ValueError(f"Expected {value!r} <= {self.maxvalue}")
            raise VE.NumberHighError(value)


class String(Validator):
    def __init__(self, minsize, maxsize, predicate):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if len(value) < self.minsize:
            # raise ValueError(f"Expected len({value!r}) >= {self.minsize}")
            raise VE.StringShortError(value)
        if len(value) > self.maxsize:
            # raise ValueError(f"Expected len({value!r}) <= {self.maxsize}")
            raise VE.StringLongError(value)
        if not self.predicate(value):
            # raise ValueError(
            #     f"Expected {self.predicate.__name__}({value!r})" f" is true"
            # )
            raise VE.StringPredicateError(value)


class Component:
    name = String(3, 10, str.isupper)
    kind = OneOf("wood", "metal", "plastic")
    quantity = Number(3, 25)

    def __init__(self, name, kind, quantity):
        self.kind = kind
        self.quantity = quantity
        self.name = name

    def __str__(self):
        return ", ".join(map(str, (self.name, self.kind, self.quantity)))


class TestComponent(unittest.TestCase):
    def test_nok10(self):
        with self.assertRaises(VE.StringPredicateError):
            Component("Widget", "metal", 5)

    def test_nok20(self):
        with self.assertRaises(VE.OneOfError):
            Component("WIDGET", "metle", 5)

    def test_nok30(self):
        with self.assertRaises(VE.NumberLowError):
            Component("WIDGET", "metal", -5)

    def test_nok40(self):
        with self.assertRaises(VE.NumberTypeError):
            Component("WIDGET", "metal", "V")

    def test_ok10(self):
        # fmt: off
        self.assertEqual(str(Component("WIDGET", "metal", 5)),
                         "WIDGET, metal, 5")
        # fmt: on


if __name__ == "__main__":
    unittest.main()
