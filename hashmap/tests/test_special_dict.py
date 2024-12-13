import pytest
from res.special_dict import SpecialDict
from res.iloc import Iloc
from res.ploc import Ploc

def test_special_dict_initialization():
    data = {"key1": 1, "key2": 2}
    special_dict = SpecialDict(data)
    assert isinstance(special_dict, SpecialDict)
    assert special_dict == data
    assert isinstance(special_dict.iloc, Iloc)
    assert isinstance(special_dict.ploc, Ploc)

def test_special_dict_invalid_initialization():
    with pytest.raises(TypeError):
        SpecialDict(["key1", "key2"])
    special_dict = SpecialDict()
    assert isinstance(special_dict, SpecialDict)
    assert special_dict == {} 

def test_special_dict_invalid_key():
    special_dict = SpecialDict({"key1": 1, "key2": 2})
    with pytest.raises(KeyError):
        special_dict["invalid_key"]