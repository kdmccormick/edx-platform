#!/usr/bin/env python3

from __future__ import annotations

import inspect
import string
import typing as t
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass
from datetime import timedelta
from io import TextIOBase
from mock import patch
from path import Path
from pprint import pprint

from django.conf import settings


SETTING_NAME_REGEX = re.compile(r'^[A-Z][A-Z0-9_]*$')

def main():
    show_cleaned()


def show_types():
    result = map_types_to_keypaths(get_settings_dict(settings))
    for typ, keypaths in sorted(result.items(), key=(lambda tk: str(tk[0]))):
        if typ in [type(None), bool, int, float, str, list, tuple, dict, set]:
            continue
        print(typ.__name__)
        for keypath in sorted(keypaths):
            print(f"\t{keypath_to_settings_ref(keypath)}")


def show_cleaned():
    #pprint(clean_settings_value(get_settings_dict(settings)))
    print(*generate_settings_module_lines(*clean_settings_value(get_settings_dict(settings))), sep="\n")


def generate_settings_module_lines(cleaned_settings, python_refs):
    return [
        "import datetime",
        "from collections import OrderedDict",
        "from path import Path",
        "",
        *sorted(set(f"import {ref.module}" for ref in python_refs)),
        "",
        *sorted(f"{key} = {value!r}" for key, value in cleaned_settings.items()),
    ]



def get_settings_dict(settings_object) -> dict[str, object]:
    return {
        name: getattr(settings, name)
        for name in dir(settings)
        if SETTING_NAME_REGEX.match(name)
    }


@dataclass(frozen=True)
class GetText:
    original: str
    def __str__(self):
        return f"_({self.original!r})"
    __repr__ = __str__


@dataclass(frozen=True)
class Lambda:
    source: str
    def __str__(self):
        return self.source
    __repr__ = __str__


@dataclass(frozen=True)
class PythonReference:
    module: str
    qualname: str
    def __str__(self):
        return f"{self.module}::{self.qualname}"
    def __repr__(self):
        return f"{self.module}.{self.qualname}"


def clean_settings_value(value: object) -> tuple[object, set[PythonReference]]:
    typ = type(value)
    if typ in (type(None), bool, int, float, str, Path, timedelta):
        return value, set()
    if typ in (list, tuple, set):
        cleaned_elements = []
        all_refs: set[PythonReference] = set()
        for element in value:
            cleaned_element, refs = clean_settings_value(element)
            cleaned_elements.append(cleaned_element)
            all_refs |= refs
        return typ(cleaned_elements), all_refs
    if typ in (OrderedDict, dict):
        cleaned_items = []
        all_refs: set[PythonReference] = set()
        for subkey, subval in value.items():
            if type(subkey) not in (str, int):
                raise ValueError(f"Unexpected dict key {subkey} of type {type(subkey)}")
            cleaned_subval, refs = clean_settings_value(subval)
            cleaned_items.append((subkey, cleaned_subval))
            all_refs |= refs
        return typ(cleaned_items), all_refs
    if proxy_args := getattr(value, "_proxy____args", None):
        # Handle strings which are wrapped in gettext_lazy
        if len(proxy_args) == 1:
            if isinstance(proxy_args[0], str):
                return GetText(proxy_args[0]), set()
        raise ValueError(f"Mysterious proxy object arguments: {proxy_args}")
    if value is sys.stderr:
        ref = PythonReference("sys", "stderr")
        return ref, {ref}
    if value.__name__  == "<lambda>":
        breakpoint()
        return Lambda(inspect.getsource(value)), set()  # TODO: any imports?
    ref = PythonReference(value.__module__, value.__qualname__)
    return ref, {ref}


Key: t.TypeAlias = str | int
KeyPath: t.TypeAlias = tuple[Key, ...]
KeyPathsByType: t.TypeAlias = dict[type, set[KeyPath]]


def keypath_to_settings_ref(keypath: KeyPath):
    subscripts = "".join(f"[{key!r}]" for key in keypath[1:])
    return f'settings.{keypath[0]}{subscripts}'



def map_types_to_keypaths(obj: object) -> KeyPathsByType:
    children: list[tuple[Key, object]]
    if isinstance(obj, dict):
        children = obj.items()
    elif isinstance(obj, (str, path.Path, TextIOBase)):
        # These are all technically enumerable, but we don't want to do that.
        children = []
    elif repr(obj.__class__) == "<class 'django.utils.functional.lazy.<locals>.__proxy__'>":
        children = []
    else:
        try:
            children = enumerate(obj)  # type: ignore[arg-type]
        except TypeError:
            children = []
    result: KeyPathsByType = {}
    for key, child in children:
        if not isinstance(key, (int, str)):
            raise ValueError(f"Key is not int or str: {key}")
        result.setdefault(type(child), set()).add((key,))
        for child_type, child_keypaths in map_types_to_keypaths(child).items():
            result.setdefault(child_type, set())
            result[child_type] |= {
                (key, *child_keypath) for child_keypath in child_keypaths
            }
    return result


if __name__ == "__main__":
    main()
