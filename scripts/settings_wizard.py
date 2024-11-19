#!/usr/bin/env python3

from __future__ import annotations

import inspect
import json
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

PYREF_NAME_KEY = "@@PYREF"
PYREF_MODULE_KEY = "@@MODULE"
PYREF_ARGS_KEY = "@@ARGS"
PYREF_KWARGS_KEY = "@@KWARGS"

def main():
    #show_json()
    #settings_json = settings_value_to_json(get_settings_dict(settings))
    #json.dump(settings_json, sys.stdout, indent=4)

    with open("production.json") as f:
        prod = json.load(f)
    with open("tutor_production.json") as f:
        tutor_prod = json.load(f)
    muts = diff_json_settings(prod, tutor_prod, [])
    for mut in muts:
        print(mut.to_python())


def show_types():
    result = map_types_to_keypaths(get_settings_dict(settings))
    for typ, keypaths in sorted(result.items(), key=(lambda tk: str(tk[0]))):
        if typ in [type(None), bool, int, float, str, list, tuple, dict, set]:
            continue
        print(typ.__name__)
        for keypath in sorted(keypaths):
            print(f"\t{keypath_to_settings_ref(keypath)}")


def show_json():
    import json, sys
    #print(*generate_settings_module_lines(*clean_settings_value(get_settings_dict(settings))), sep="\n")


def show_python():
    settings_json = settings_value_to_json(get_settings_dict(settings))


@dataclass(frozen=True)
class Mut:
    path: list[str]

    @property
    def ref(self):
        return self.path[0] + "".join(f"[{path_part!r}]" for path_part in self.path[1:])
    def to_python(self) -> str:
        raise NotImplementedError

@dataclass(frozen=True)
class PushLeft(Mut):
    value: object
    def to_python(self):
        return f"{self.ref}.insert(0, {self.value!r})"

@dataclass(frozen=True)
class PushRight(Mut):
    value: object
    def to_python(self):
        return f"{self.ref}.append({self.value!r})"

@dataclass(frozen=True)
class PopLeft(Mut):
    value: object
    def to_python(self):
        return f"{self.ref}.pop(0)"

@dataclass(frozen=True)
class PopRight(Mut):
    value: object
    def to_python(self):
        return f"{self.ref}.pop()"

@dataclass(frozen=True)
class Update(Mut):
    value: object
    def to_python(self):
        return f"{self.ref} = {self.value!r}"


@dataclass(frozen=True)
class Delete(Mut):
    pass
    def to_python(self):
        return f"del {self.ref}"


l1 = [     "b", "c",    , "f1"]
l2 = ["a", "b",      "d", "f2", "g"]





def diff_json_settings(json1: object, json2: object, path: list[str | int]) -> list[Mut]:
    if json1 == json2:
        return []
    if isinstance(json1, list) and isinstance(json2, list):
        update_muts = None
        list_muts = None
        if len(json1) == len(json2):
            update_muts = [
                Update([*path, i], json2[i])
                for i in len(json1) if json1[i] != json2[i]
            ]
        best_left1 = None
        best_left2 = None
        best_length = 0
        for left1 in range(0, len(json1)):
            for left2 in range(i1, len(json2)):
                right1 = left1
                right2 = left2
                length = 0
                while right1 < len(json1) and right2 < len(json2) and json1[right1] == json2[right2]:
                    right1 += 1
                    right2 += 1
                    length += 1
                if length > best_length:
                    best_left1 = left1
                    best_left2 = left2
                    best_length = length
        if best_length:
            list_muts = [
                *(PopLeft(path) for _ in range(best_left1)),
                *(PopRight(path) for _ in range(best_left2 + best_length, len(json1))),
                *(PushLeft(path, value) for value in json2[:best_left2]),
                *(PushRight(path, value) for value in json2[(best_left2 + best_overlap):]),
            ]
        if len(list_muts) < len(json2) and len(list_muts) < list(update_muts):
            return list_muts
        elif len(update_muts) < len(json2):
            return update_muts


        if len(update_muts) < len(json2) and len(update_muts) <
        append_muts = [
            Append(path, json[i]) for i in range(
        ]

        if len(json1) < len(json2):
            ix = 0
            while ix < len(json1):
                if json1[ix] != json2[ix]:
                    break
                ix += 1
            if ix > 0:
                return [Append(path, json2[i]) for i in range(ix, len(json2))]
        if False and len(json1) == len(json2):  # @@TODO
            ele_replacements = []
            for ix, ele1 in enumerate(json1):
                if ele1 == (ele2 := json2[ix]):
                    ele_replacements.append(Replace([*path, ix], ele2))
            if len(ele_rplacements) < len(json1):
                return ele_replacements

    if isinstance(json1, dict) and isinstance(json2, dict) and PYREF_NAME_KEY not in json1:
        muts = []
        kept_something = False
        for key in json1:
            if key not in json2:
                muts += [Delete([*path, key])]
        for key in json2:
            if key in json1:
                if json1[key] == json2[key]:
                   kept_something = True
                else:
                   muts += diff_json_settings(json1[key], json2[key], [*path, key])
            else:
                muts += [Update([*path, key], json2[key])]
        if kept_something:
            return muts
    return [Update(path, json2)]


def generate_settings_module_lines(cleaned_settings, python_refs):
    result = []

    return [
        "import datetime",
        "from collections import OrderedDict",
        "from path import Path",
        "from path import Path",
        "",
        "from django.utils.translation import gettext_lazy as _",
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


def json_pyref(module: str | None, name: str, args: tuple | None, kwargs: dict | None) -> dict:
    return {
        PYREF_NAME_KEY: name,
        **({} if module is None else {PYREF_MODULE_KEY: module}),
        **({} if args is None else {PYREF_ARGS_KEY: list(args)}),
        **({} if kwargs is None else {PYREF_KWARGS_KEY: kwargs}),
    }


@dataclass(frozen=True)
class LiteralPython:
    code: str
    def __str__(self):
        return self.code
    __repr__ = __str__


def json_to_settings_value(json: object, modules_to_import: set[str]) -> object:
    if isinstance(json, dict):
        if ref_name := json.get(PYREF_NAME_KEY):
            code = ref_name
            if ref_module := json.get(PYREF_MODULE_KEY):
                modules_to_import.add(ref_module)
                code = f"{ref_module}.{code}"
            if (
                (ref_args := json.get(PYREF_ARGS_KEY)) is not None or
                (ref_kwargs := json.get(PYREF_ARGS_KEY)) is not None
            ):
                code += "(" + ", ".join(
                    *(
                        json_to_settings_value(arg, module_to_import)
                        for arg in ref_args or []
                    ),
                    *(
                        f"{key}={json_to_settings_value(val, modules_to_import)}"
                        for key, val in (ref_kwargs or {}).items()
                    ),
                ) + ")"
            return LiteralPython(code)
        return {key: json_to_settings_value(val) for key, val in json.items()}
    if isinstance(json, list):
        return [json_to_settings_value(element, modules_to_import) for element in json]
    return json


def settings_value_to_json(value: object) -> object:
    if isinstance(value, (type(None), bool, int, float, str)):
        return value
    if isinstance(value, Path):
        return json_pyref("path", "Path", str(value), None)   # @@TODO ensure correct subtype?
    if isinstance(value, timedelta):
        return json_pyref("datetime", "timedelta", None, {
            "seconds": value.total_seconds(),
            "microseconds": value.microseconds,
        })
    if isinstance(value, (list, tuple, set)):
        return [settings_value_to_json(element) for element in value]
    if isinstance(value, set):
        return json_pyref(None, "set", args=[[settings_value_to_json(element) for element in value]])
    if isinstance(value, dict):
        for subkey in value.keys():
            if not isinstance(subkey, (str, int)):
                raise ValueError(f"Unexpected dict key {subkey} of type {type(subkey)}")
        return {subkey: settings_value_to_json(subval) for subkey, subval in value.items()}
    if proxy_args := getattr(value, "_proxy____args", None):
        # Handle strings which are wrapped in gettext_lazy
        if len(proxy_args) == 1:
            if isinstance(proxy_args[0], str):
                return json_pyref("django.contrib.translation.utils", "gettext_lazy", [proxy_args[0]], None)
        raise ValueError(f"Mysterious proxy object arguments: {proxy_args}")
    if value is sys.stderr:
        return json_pyref("sys", "stderr", None, None)
    try:
        ref_module = value.__module__
        ref_qualname = value.__qualname__
    except AttributeError:
        raise ValueError("Cannot handle setting value {ref!r} of type {type(ref)}")
    if ref_qualname == "<lambda>":
        return json_pyref(None, "TODO_FillInThisLambda", None, {"hint": inspect.getsource(value).strip()})
    return json_pyref(ref_module, ref_qualname, None, None)


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
