from .parser import Parser
from .token import Token, TokenType
from .ast import Number, Condition

def operator(cond: Condition, num: Token):
    if cond.op.value == '>':
        return int(num.value) > int(cond.right.token.value)
    elif cond.op.value == '<':
        return int(num.value) < int(cond.right.token.value)
    elif cond.op.value == '>=':
        return int(num.value) >= int(cond.right.token.value)
    elif cond.op.value == '<=':
        return int(num.value) <= int(cond.right.token.value)
    elif cond.op.value == '=':
        return int(num.value) == int(cond.right.token.value)
    elif cond.op.value == '<>':
        return int(num.value) != int(cond.right.token.value)
    else:
        raise SyntaxError(f"Invalid operator: {cond.op.value}")

class Ploc(dict):
    def __init__(self, dictionary: dict):
        self.sdict = dictionary
        self.parser = Parser()
    
    def getitem(self, cond):
        if not isinstance(cond, str):
            raise TypeError("The condition must be a string")
        if not cond:
            return {}

        tree = self.parser.parse(cond)
        size = len(tree)
        list_keys = []

        for k in self.sdict.keys():
            if k.isdigit() or (k[0] == '(' and k[-1] == ')'):
                res = self.parser.parse(k)
                if len(res) == size:
                    list_keys.append((k, res))

        result = {}

        for k, parsed_key in list_keys:
            count = 0
            for j in range(size):
                if operator(tree[j], parsed_key[j].right.token):
                    count += 1
            if count == size:
                result[k] = self.sdict[k]
        return result
