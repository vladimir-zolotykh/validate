#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import unittest
import validator_data as VD
import validator_error as VE


class OneOf(VD.OneOf0):
    def validate(self, value):
        if value not in self.options:
            raise VE.OneOfError(value, data=self)


class Number(VD.Number0):
    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise VE.NumberTypeError(value, data=self)
        if value < self.minvalue:
            raise VE.NumberLowError(value, data=self)
        if self.maxvalue < value:
            raise VE.NumberHighError(value, data=self)


class String(VD.String0):
    def validate(self, value):
        if len(value) < self.minsize:
            raise VE.StringShortError(value, data=self)
        if len(value) > self.maxsize:
            raise VE.StringLongError(value, data=self)
        if not self.predicate(value):
            raise VE.StringPredicateError(value, data=self)


class Component:
    name = String(3, 10, str.isupper)
    kind = OneOf("wood", "metal", "plastic")
    quantity = Number(3, 25)  # Number(3, 25, (int, float))

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
            # validator_error.NumberLowError: Expected -5 >= 3
            Component("WIDGET", "metal", -5)

    def test_nok35(self):
        with self.assertRaises(VE.NumberHighError):
            # NumberHighError: Expected 100 <= 25
            Component("WIDGET", "metal", 100)

    def test_nok40(self):
        with self.assertRaises(VE.NumberTypeError):
            # NumberTypeError: Expected 'V' of type int or float
            Component("WIDGET", "metal", "V")

    def test_nok45(self):
        with self.assertRaises(VE.StringShortError):
            Component("WI", "metal", 3)

    def test_nok50(self):
        with self.assertRaises(VE.StringLongError):
            Component("SCHIZOPHRENIA", "metal", 3)

    def test_nok55(self):
        with self.assertRaises(VE.StringPredicateError):
            Component("Widget", "metal", 3)

    def test_ok10(self):
        # fmt: off
        self.assertEqual(str(Component("WIDGET", "metal", 5)),
                         "WIDGET, metal, 5")
        # fmt: on


if __name__ == "__main__":
    unittest.main()
