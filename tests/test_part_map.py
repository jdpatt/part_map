from pathlib import Path

import pytest
from part_map.part_map import PartObject


def test_load_from_excel():
    obj = PartObject.from_excel(
        Path(__file__).parent.parent.joinpath("examples", "artix7_example.xlsx")
    )
    assert obj.get_number_of_pins() == 238


def test_load_from_json():
    obj = PartObject.from_json(
        Path(__file__).parent.parent.joinpath("examples", "connector_example.json")
    )
    assert obj.get_number_of_pins() == 58


def test_get_columns():
    obj = PartObject.from_json(
        Path(__file__).parent.parent.joinpath("examples", "connector_example.json")
    )
    assert obj.get_columns() == [str(x) for x in range(1, 17)]


def test_get_rows():
    obj = PartObject.from_json(
        Path(__file__).parent.parent.joinpath("examples", "connector_example.json")
    )
    assert obj.get_rows() == ["A", "B", "C", "D"]


def test_add_pin():
    obj = PartObject({}, "TestObject")
    obj.add_pin("A1", "TEST", "0xFFFFFF")
    assert list(obj.get_pins()) == ["A1"]
