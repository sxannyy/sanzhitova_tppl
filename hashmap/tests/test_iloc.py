import pytest
from res.iloc import Iloc

def test_iloc_getitem():
    iloc = Iloc({"a": 1, "b": 2, "c": 3})
    assert iloc[0] == 1
    assert iloc[2] == 3

    with pytest.raises(TypeError):
        iloc["invalid"]

    with pytest.raises(ValueError):
        iloc[5]

def test_iloc_sorted_keys():
    iloc = Iloc({"c": 3, "a": 1, "b": 2})
    assert iloc.sorted_keys == ["a", "b", "c"]