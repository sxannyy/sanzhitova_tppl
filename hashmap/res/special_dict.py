from .iloc import Iloc
from .ploc import Ploc

class SpecialDict(dict):
    def __init__(self, dictionary = None):
        if dictionary and not isinstance(dictionary, dict):
            raise TypeError("The dictionary wasn't transmitted!")
        if dictionary is None:
            dictionary = {}
        super().__init__(dictionary)

        self.iloc = Iloc(self)
        self.ploc = Ploc(self)