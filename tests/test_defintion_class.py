import pytest

from magic_specs import Definition


def test_definition():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3
        D = 4

    assert str(Foo) == "{A=1, B=2, C=3, D=4}"
    assert len(Foo) == 4

    assert Foo.A == 1
    assert Foo.B == 2
    assert Foo.C == 3
    assert Foo.D == 4

    assert Foo["A"] == 1
    assert Foo["B"] == 2
    assert Foo["C"] == 3
    assert Foo["D"] == 4

    assert Foo(1) == "A"
    assert Foo(2) == "B"
    assert Foo(3) == "C"
    assert Foo(4) == "D"


def test_definition__missing_key_or_value():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3
        D = 4

    with pytest.raises(AttributeError):
        assert Foo.Bar == 5  # type: ignore

    with pytest.raises(KeyError):
        assert Foo["Bar"] == 5

    with pytest.raises(KeyError):
        assert Foo(5) == "Bar"


def test_definition__missing_key__default():
    class Foo(Definition, default_key=None):
        A = 1

    assert Foo._default_key_ is None

    assert Foo(5) is None


def test_definition__missing_value__default():
    class Foo(Definition, default_value=None):
        A = 1

    assert Foo._default_value_ is None

    assert Foo["Bar"] is None

    # Attribute access still throws an error
    with pytest.raises(AttributeError):
        assert Foo.Bar is None  # type: ignore


def test_definition__cannot_instantiate():
    with pytest.raises(TypeError):
        Definition()

    class Foo(Definition):
        A = 1

    with pytest.raises(TypeError):
        Foo()


def test_definition__immutability():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3
        D = 4

    msg = "Definition cannot be changed once created."

    with pytest.raises(AttributeError, match=msg):
        Foo.Bar = 5

    with pytest.raises(AttributeError, match=msg):
        del Foo.Bar

    # Internal values should also not be overridable
    with pytest.raises(AttributeError, match=msg):
        Foo._value2key_map_ = 5

    with pytest.raises(AttributeError, match=msg):
        del Foo._value2key_map_


def test_definition__membership_tests():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3
        D = 4

    assert "A" in Foo
    assert "Bar" not in Foo

    assert "A" in Foo.keys()
    assert 1 in Foo.values()


def test_definition__annotated():
    class Foo(Definition):
        A: int = 1
        B: int = 2
        C: int = 3
        D: int = 4

    assert str(Foo) == "{A=1, B=2, C=3, D=4}"

    assert Foo.A == 1
    assert Foo.B == 2
    assert Foo.C == 3
    assert Foo.D == 4

    assert Foo(1) == "A"
    assert Foo(2) == "B"
    assert Foo(3) == "C"
    assert Foo(4) == "D"


def test_definition__unique_keys():
    with pytest.raises(ValueError, match="'A' and 'C' have the same value: 1"):

        class Foo(Definition):
            A = 1
            B = 2
            C = 1


def test_definition__not_unique():
    class Foo(Definition, unique=False):
        A = 1
        B = 1
        C = 2
        D = 2

    assert Foo.A == 1
    assert Foo.B == 1
    assert Foo.C == 2
    assert Foo.D == 2

    assert Foo["A"] == 1
    assert Foo["B"] == 1
    assert Foo["C"] == 2
    assert Foo["D"] == 2

    msg = "Non unique-valued Definitions do not support reverse lookups."

    with pytest.raises(TypeError, match=msg):
        Foo(1)

    with pytest.raises(TypeError, match=msg):
        Foo(2)

    with pytest.raises(TypeError, match=msg):
        Foo(3)


def test_definition__imported():
    # Check that importing doesn't break anything internal
    from .conftest import TestDefinition

    assert TestDefinition.foo == 1
    assert TestDefinition.bar == 2

    assert TestDefinition(1) == "foo"
    assert TestDefinition(2) == "bar"


def test_definition__inheritance():
    class Foo(Definition):
        A = 1
        B = 2

    class Bar(Foo):
        C = 3
        D = 4

    assert str(Foo) == "{A=1, B=2}"
    assert str(Bar) == "{A=1, B=2, C=3, D=4}"


def test_definition__inheritance__to_not_unique():
    class Foo(Definition):
        A = 1
        B = 2

    class Bar(Foo, unique=False):
        C = 1
        D = 2

    assert str(Foo) == "{A=1, B=2}"
    assert str(Bar) == "{A=1, B=2, C=1, D=2}"


def test_definition__inheritance__two_base_classes():
    class Foo(Definition):
        A = 1
        B = 2

    class Bar(Definition):
        C = 3
        D = 4

    class FooBar(Foo, Bar):
        E = 5

    assert str(FooBar) == "{A=1, B=2, C=3, D=4, E=5}"


def test_definition__inheritance__base_classes_have_common_keys():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3

    class Bar(Definition):
        C = 3
        D = 4

    with pytest.raises(ValueError, match="'Foo' and 'Bar' both defined 'C'"):

        class FooBar1(Foo, Bar):
            A = 1
            B = 2

    # unique only affects values, not keys
    with pytest.raises(ValueError, match="'Foo' and 'Bar' both defined 'C'"):

        class FooBar2(Foo, Bar, unique=False):
            A = 1
            B = 2

    with pytest.raises(ValueError, match="'Foo' already defined 'A'"):

        class Baz(Foo):
            A = 1
            B = 2


def test_definition__inheritance__base_classes_have_common_values():
    class Foo(Definition):
        A = 1
        B = 2

    class Bar(Definition):
        C = 3
        D = 2

    with pytest.raises(ValueError, match="'B' and 'D' have the same value: 2"):

        class FooBar1(Foo, Bar):
            E = 1
            F = 2

    # unique=False allows unique values from base classes as well
    class FooBar2(Foo, Bar, unique=False):
        E = 1
        F = 2

    assert str(FooBar2) == "{A=1, B=2, C=3, D=2, E=1, F=2}"

    with pytest.raises(ValueError, match="'A' and 'E' have the same value: 1"):

        class Baz(Foo):
            E = 1
            F = 2


def test_definition__other_definitions_as_values():
    class Foo(Definition):
        A = 1
        B = 2

    class Bar(Definition):
        C = 3
        D = 4

    class FooBar(Definition):
        foo = Foo
        bar = Bar

    assert FooBar.foo == Foo
    assert FooBar.bar == Bar

    assert FooBar.foo.A == 1
    assert FooBar.bar.C == 3

    assert FooBar.foo(2) == "B"
    assert FooBar.bar(4) == "D"


def test_definition__definition_inception():
    class FooBar(Definition):
        class Foo(Definition):
            A = 1
            B = 2

        class Bar(Definition):
            C = 3
            D = 4

    assert FooBar.Foo.A == 1
    assert FooBar.Bar.C == 3

    assert FooBar.Foo(2) == "B"
    assert FooBar.Bar(4) == "D"


def test_definition__definitions_are_not_special_values():
    class Foo(Definition):
        A = 1
        B = 2

    with pytest.raises(ValueError, match="'Foo' already defined 'B'"):

        class Bar(Foo):
            class B(Definition):
                A = 1
                B = 2


def test_definition__unhashable_values():

    msg = r"'.+' is not hashable, and thus cannot be used for uniquely-valued Definitions."

    with pytest.raises(ValueError, match=msg):

        class Foo(Definition):
            A = {"foo": 1, "bar": 2}

    with pytest.raises(ValueError, match=msg):

        class Bar(Definition):
            A = ["foo", "bar"]

    with pytest.raises(ValueError, match=msg):

        class Baz(Definition):
            A = {"foo", "bar"}


def test_definition__unhashable_values__non_unique_valued_definitions():
    class Foo(Definition, unique=False):
        A = {"foo": 1, "bar": 2}

    class Bar(Definition, unique=False):
        A = ["foo", "bar"]

    class Baz(Definition, unique=False):
        A = {"foo", "bar"}

    assert Foo.A == {"foo": 1, "bar": 2}
    assert Bar.A == ["foo", "bar"]
    assert "foo" in Baz.A and "bar" in Bar.A


def test_definition__inheritance__unhashable_values():
    class Foo(Definition, unique=False):
        A = {"foo": 1, "bar": 2}

    class Bar(Definition, unique=False):
        A = ["foo", "bar"]

    class Baz(Definition, unique=False):
        A = {"foo", "bar"}

    msg = r"'.+' is not hashable, and thus cannot be used for uniquely-valued Definitions."

    with pytest.raises(ValueError, match=msg):

        class FooBar1(Foo):
            B = 1

    with pytest.raises(ValueError, match=msg):

        class FooBar2(Bar):
            B = 1

    with pytest.raises(ValueError, match=msg):

        class FooBar3(Baz):
            B = 1


def test_definition__tuple_values():
    class Foo(Definition):
        A = ("foo", "bar")
        B = (1, 2)

    assert Foo.A == ("foo", "bar")
    assert Foo.B == (1, 2)


def test_definition__iterate():
    class Foo(Definition):
        A = 1
        B = 2
        C = 3
        D = 4

    assert list(Foo) == ["A", "B", "C", "D"]
    # Should work a second time too
    assert list(Foo) == ["A", "B", "C", "D"]
