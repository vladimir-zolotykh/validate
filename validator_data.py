#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterable
from abc import ABC, abstractmethod


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


class OneOf0(Validator):
    def __init__(self, *options: str):
        self.options: set[str] = set(options)


class Number0(Validator):
    def __init__(self, minvalue=0, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue


class String0(Validator):
    def __init__(self, minsize, maxsize, predicate):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate
