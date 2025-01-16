def parse_negative_numbers(expression):
    """Handle negative numbers in a mathematical expression."""
    result = []
    i = 0
    while i < len(expression):
        if expression[i] == '-' and (i == 0 or expression[i - 1] in "+-*/^("):
            # This is a negative number
            number = "-"
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                number += expression[i]
                i += 1
            result.append(float(number))
        elif expression[i].isdigit() or expression[i] == '.':
            number = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                number += expression[i]
                i += 1
            result.append(float(number))
        else:
            result.append(expression[i])
            i += 1
    return result
