import re
from importlib import import_module
from unittest.mock import patch

import pytest

from magic_specs import import_from_string


def func():
    pass


def test_import_from_string():
    with patch("magic_specs._import_from_string.import_module", side_effect=import_module) as patched:
        f = import_from_string("tests.test_import_from_string.func")

    assert patched.call_count == 0

    assert f == func


def test_import_from_string__not_in_modules():
    with patch("magic_specs._import_from_string.import_module", side_effect=import_module) as patched:
        f = import_from_string("tests.noimport.foo")

    assert patched.call_count == 1

    from .noimport import foo

    assert f == foo


@pytest.mark.parametrize(
    ["import_string", "error"],
    [
        ["tests", "Could not import 'tests': Not a valid module path."],
        ["tests.foo", "Could not import 'tests.foo': Module 'tests' does not define 'foo'."],
        ["tests.foo", "Could not import 'tests.foo': Module 'tests' does not define 'foo'."],
        ["tests.noimport.x", "Could not import 'tests.noimport.x': Module 'tests.noimport' does not define 'x'."],
        ["tests.no.exist", "Could not import 'tests.no.exist': No module named 'tests.no'."],
    ],
)
def test_import_from_string__import_errors(import_string, error):
    with pytest.raises(ImportError, match=re.escape(error)):
        import_from_string(import_string)
