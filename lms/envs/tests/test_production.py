"""
Test that lms/envs/production.py loads as expected.
"""
import inspect
import json
import re
import sys
from datetime import timedelta
from importlib.resources import files
from path import Path

from django.conf import settings
from django.test import TestCase


SETTING_NAME_REGEX = re.compile(r'^[A-Z][A-Z0-9_]*$')

PYREF_NAME_KEY = "@@PYREF"
PYREF_ARGS_KEY = "@@ARGS"
PYREF_KWARGS_KEY = "@@KWARGS"


class ProductionSettingsTest(TestCase):
    """
    """
    maxDiff = None

    def test_minimal_yaml(self):
        """
        """
        with open(Path(__file__).parent / "settings_snapshot.json") as f:
            expected_json = json.load(f)
        actual_json = _settings_value_to_json(get_settings_dict(settings))
        assert expected_json == actual_json


def get_settings_dict(settings_object) -> dict[str, object]:
    """
    TODO
    """
    return {
        name: getattr(settings, name)
        for name in dir(settings)
        if SETTING_NAME_REGEX.match(name)
    }


def _settings_value_to_json(value: object) -> object:
    """
    TODO
    """
    if isinstance(value, (type(None), bool, int, float, str)):
        return value
    if isinstance(value, Path):
        return _json_pyref("path.Path", str(value), None)
    if isinstance(value, timedelta):
        return _json_pyref("datetime.timedelta", None, {
            "seconds": value.total_seconds(),
            "microseconds": value.microseconds,
        })
    if isinstance(value, (list, tuple)):
        return [_settings_value_to_json(element) for element in value]
    if isinstance(value, set):
        return _json_pyref("set", [sorted(_settings_value_to_json(element) for element in value)], None)
    if isinstance(value, dict):
        for subkey in value.keys():
            if not isinstance(subkey, (str, int)):
                raise ValueError(f"Unexpected dict key {subkey} of type {type(subkey)}")
        return {subkey: _settings_value_to_json(subval) for subkey, subval in value.items()}
    if proxy_args := getattr(value, "_proxy____args", None):
        # Handle strings which are wrapped in gettext_lazy
        if len(proxy_args) == 1:
            if isinstance(proxy_args[0], str):
                return _json_pyref("django.contrib.translation.utils.gettext_lazy", [proxy_args[0]], None)
        raise ValueError(f"Mysterious proxy object arguments: {proxy_args}")
    if value is sys.stderr:
        return _json_pyref("sys.stderr", None, None)
    try:
        ref_module = value.__module__
        ref_qualname = value.__qualname__
    except AttributeError:
        breakpoint()
        raise ValueError(f"Cannot handle setting value {value!r} of type {type(value)}")
    if ref_qualname == "<lambda>":
        # TODO
        return _json_pyref("<lambda>", None, {"hint": inspect.getsource(value).strip()})
    return _json_pyref(f"{ref_module}.{ref_qualname}", None, None)


def _json_pyref(qualname: str, args: tuple | None, kwargs: dict | None) -> dict:
    """
    """
    return {
        PYREF_NAME_KEY: qualname,
        **({} if args is None else {PYREF_ARGS_KEY: list(args)}),
        **({} if kwargs is None else {PYREF_KWARGS_KEY: kwargs}),
    }

