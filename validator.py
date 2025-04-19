#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import unittest


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
            raise ValueError(f"Expected {value!r} be one of {self.options}")


class Number(Validator):
    def __init__(self, minvalue=0, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected {value!r} of type int or float")
        if value < self.minvalue:
            raise ValueError(f"Expected {value!r} >= {self.minvalue}")
        if self.maxvalue < value:
            raise ValueError(f"Expected {value!r} <= {self.maxvalue}")


class String(Validator):
    def __init__(self, minsize, maxsize, predicate):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if len(value) < self.minsize:
            raise ValueError(f"Expected len({value!r}) >= {self.minsize}")
        if len(value) > self.maxsize:
            raise ValueError(f"Expected len({value!r}) <= {self.maxsize}")
        if not self.predicate(value):
            raise ValueError(f"Expected {self.predicate}({value}) is true")


class Component:
    kind = OneOf("wood", "metal", "plastic")
    quantity = Number(3, 25)
    name = String(3, 10, str.isupper)

    def __init__(self, kind, quantity, name):
        self.kind = kind
        self.quantity = quantity
        self.name = name

    def __str__(self):
        return ", ".join(map(str, (self.kind, self.quantity, self.name)))


class TestComponent(unittest.TestCase):
    def test_nok1(self):
        with self.assertRaises(TypeError):
            Component("wood", "10", "FOO")

    def test_nok2(self):
        with self.assertRaises(ValueError):
            Component("Widget", "metal", 5)

    def test_nok3(self):
        with self.assertRaises(ValueError):
            Component("WIDGET", "metle", 5)

    def test_nok4(self):
        with self.assertRaises(ValueError):
            Component("WIDGET", "metal", -5)

    def test_ok1(self):
        self.assertEqual(str(Component("wood", 10, "FOO")), "wood, 10, FOO")


if __name__ == "__main__":
    unittest.main()
