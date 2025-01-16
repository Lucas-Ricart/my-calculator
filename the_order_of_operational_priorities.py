def apply_operation(op, a, b):
    """Apply a mathematical operation between two numbers."""
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
    elif op == '^':
        return a ** b

def evaluate_simple(expression):
    """Evaluate an expression without parentheses, respecting operator precedence."""
    priorities = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    numbers = []
    operators = []

    i = 0
    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':  # Read a number
            number = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                number += expression[i]
                i += 1
            numbers.append(float(number))
            continue

        elif expression[i] in priorities:  # Read an operator
            while operators and priorities[operators[-1]] >= priorities[expression[i]]:
                op = operators.pop()
                b = numbers.pop()
                a = numbers.pop()
                numbers.append(apply_operation(op, a, b))
            operators.append(expression[i])
        
        i += 1

    # Apply remaining operators
    while operators:
        op = operators.pop()
        b = numbers.pop()
        a = numbers.pop()
        numbers.append(apply_operation(op, a, b))

    return numbers[0]
