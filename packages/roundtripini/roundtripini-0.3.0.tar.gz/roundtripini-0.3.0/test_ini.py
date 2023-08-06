# Copyright 2021 Benjamin Winger
# Distributed under the terms of the GNU General Public License v3

import pytest
from io import StringIO

from roundtripini import INI


def test_simple_ini():
    """Tests that simple files can be read and written while preserving formatting"""
    file = """
[section]
key = value
other key=other value
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == "value"
    assert ini["section", "other key"] == "other value"
    assert ini.dump() == file


def test_ini_modification():
    """Tests that the file can be modified while still preserving formatting"""
    file = """
# Comment

[section]
# Comment
key = value
other key=other value
"""

    changed_file = """
# Comment

[section]
# Comment
key = new value
other key = other value
"""

    ini = INI(StringIO(file))
    ini["section", "key"] = "new value"
    ini["section", "other key"] = "other value"
    assert ini["section", "key"] == "new value"
    assert ini["section", "other key"] == "other value"
    assert ini.dump() == changed_file


def test_simple_duplicate_keys():
    """Tests that duplicate keys are supported"""
    file = """
[section]
key = value
key = value 2
"""

    changed_file = """
[section]
key = value
key = value 2
key = value 3
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == ["value", "value 2"]
    ini["section", "key"] = ini["section", "key"] + ["value 3"]
    assert ini["section", "key"] == ["value", "value 2", "value 3"]
    assert ini.dump() == changed_file


def test_simple_duplicate_sections():
    """Tests that duplicate sections are supported"""
    file = """
[section]
key = value

[section]
key = value 2
"""

    changed_file = """
[section]
key = value
key = value 2
key = value 3

[section]
"""

    ini = INI(StringIO(file))
    assert ini["section", "key"] == ["value", "value 2"]
    ini["section", "key"] = ini["section", "key"] + ["value 3"]
    assert ini["section", "key"] == ["value", "value 2", "value 3"]
    assert ini.dump() == changed_file


def test_add_section():
    """Tests that inserting new sections works"""

    file = """
[section]
key = value
"""

    changed_file = """
[section]
key = value
[section 2]
key = value
"""

    ini = INI(StringIO(file))
    ini["section 2", "key"] = "value"
    assert ini["section", "key"] == "value"
    assert ini["section 2", "key"] == "value"
    assert ini.dump() == changed_file


def test_iter():
    """Tests that iterating over sections works"""

    file = """
[section]
key = value
[section 2]
key = value
"""
    ini = INI(StringIO(file))
    assert list(ini) == [None, "section", "section 2"]


def test_iter_keys():
    """Tests that iterating over sections and keys works"""

    file = """
[section]
key = value
[section 2]
key = value
key2 = value2
[section]
key3 = value3
"""
    ini = INI(StringIO(file))
    assert not list(ini.keys(None))
    assert list(ini.keys("section")) == ["key", "key3"]
    assert list(ini.keys("section 2")) == ["key", "key2"]


def test_missing():
    """Tests that missing elements are handled correctly"""
    ini = INI(StringIO(""))
    assert ini["section", "key"] is None


def test_bad_section():
    """Tests that poorly formatted sections raise an error"""
    with pytest.raises(RuntimeError):
        INI(StringIO("[foo"))


def test_bad_entry():
    """Tests that poorly formatted entries raise an error"""
    ini = INI(StringIO("[foo]\nbar baz baf"))
    with pytest.raises(RuntimeError):
        ini["foo", "bar"]


def test_append_key():
    """Tests that appending a key to existing sections works"""
    ini = INI(StringIO("[foo]\n"))
    ini["foo", "bar"] = "baz"
    assert ini.dump() == """[foo]
bar = baz
"""

def test_append_key_no_line_ending():
    """Tests that appending a key to existing sections works"""
    ini = INI(StringIO("[foo]"))
    ini["foo", "bar"] = "baz"
    assert ini.dump() == """[foo]
bar = baz
"""
