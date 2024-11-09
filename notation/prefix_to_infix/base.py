def is_operator(token):
    return token in ['+', '-', '*', '/']

def prefix_to_infix(expression: str) -> str:
    tokens = expression.split()[::-1]
    stack = []
    
    for token in tokens:
        if token.isdigit():
            stack.append(token)
        elif is_operator(token):
            if len(stack) < 2:
                raise ValueError("Некорректное выражение: Вы ввели недостаточно операндов для операции.")
            oper1 = stack.pop()
            oper2 = stack.pop()
            stack.append(f"({oper1} {token} {oper2})")
        else:
            raise ValueError(f"Некорректный операнд: {token}")
    
    if len(stack) != 1:
        raise ValueError("Некорректное выражение: присутствубт лишние операнды.")
    
    return stack[0]