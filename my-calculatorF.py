import tkinter as tk
import customtkinter as ctk
import re
import json

# Constants for mathematical calculations
PI = 3.141592653589793
E = 2.718281828459045

# Initialize history
history = {}
reset_history = {}
count = 1

# Function to compute the sine of an angle (in radians) using the Taylor series
def sin(x):
    x = x % (2 * PI)  # Reduce angle to the range [0, 2π]
    result, term, n = x, x, 1
    while abs(term) > 1e-10:  # Continue until the term is very small
        term *= -x**2 / ((2 * n) * (2 * n + 1))  # Compute the next term in the series
        result += term
        n += 1
    return result

# Function to compute the cosine of an angle (in radians) using the Taylor series
def cos(x):
    x = x % (2 * PI)  # Reduce angle to the range [0, 2π]
    result, term, n = 1, 1, 1
    while abs(term) > 1e-10:  # Continue until the term is very small
        term *= -x**2 / ((2 * n - 1) * (2 * n))  # Compute the next term in the series
        result += term
        n += 1
    return result

# Function to compute the tangent of an angle (in radians)
def tan(x):
    cos_val = cos(x)  # Get the cosine of x
    if abs(cos_val) < 1e-10:  # If cosine is very close to zero, tangent is undefined
        return "Error: tan undefined"
    return sin(x) / cos_val  # Return the sine divided by the cosine

# Function for factorial
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

# Function for the exponential (e^x) using the series
def exp(x):
    result, term, n = 1, 1, 1
    while abs(term) > 1e-10:  # Continue until the term is very small
        term *= x / n  # Compute the next term in the series
        result += term
        n += 1
    return result

# Function for natural logarithm (ln(x)) using the series
def ln(x):
    if x <= 0:
        return "Error: ln of non-positive value"
    z = (x - 1) / (x + 1)
    term, result, n = z, 0, 1
    while abs(term) > 1e-10:
        result += term / n
        term *= z * z
        n += 2
    return 2 * result

# Function for log base 10
def log(x):
    return ln(x) / ln(10)

# Function to evaluate mathematical expressions
def calculate(expression):
    def evaluate_function(expression):
        match = re.search(r'([a-z]+)\(([^()]+)\)', expression)
        if match:
            func, value = match.groups()
            value = float(evaluate(value))  # Recursively evaluate the inner value
            if func == 'sin':
                result = sin(value)
            elif func == 'cos':
                result = cos(value)
            elif func == 'tan':
                result = tan(value)
            elif func == 'ln':
                result = ln(value)
            elif func == 'log':
                result = log(value)
            elif func == 'exp':
                result = exp(value)
            else:
                return f"Error: Unknown function '{func}'"
            return expression.replace(f'{func}({value})', str(result))
        return expression

    def evaluate(expression):
        expression = re.sub(r'\bpi\b', str(PI), expression)
        expression = re.sub(r'\be\b', str(E), expression)
        expression = re.sub(r'(\d)\(', r'\1*(', expression)
        expression = expression.replace("^", "**")  # Replace `^` with `**` for power
        expression = evaluate_function(expression)
        return eval(expression)

    try:
        return evaluate(expression)
    except Exception as e:
        return f"Error: {e}"

# Format result to remove unnecessary decimals
def format_result(result):
    if isinstance(result, float):
        if result.is_integer():
            return int(result)  # Remove decimal point if the number is an integer
        else:
            return result  # Keep as float if it's not an integer
    return result  # Return as is if it's not a number

# Function to clear the expression display
def clear_display():
    entry_var.set("")  # Clear the display

# Function to append a value to the expression
def append_to_display(value):
    current = entry_var.get()
    entry_var.set(current + str(value))  # Append value to current display

# Function to calculate and display the result
def calculate_and_display():
    expression = entry_var.get()
    result = calculate(expression)
    formatted_result = format_result(result)
    entry_var.set(formatted_result)  # Show the result on the display
    # Save the result to history if no error occurred
    if "Error" not in str(result):
        save_history(expression, result)

# Function to save the history
def save_history(expression, result):
    global count
    key = f"Calcul{count}"
    history[key] = {"Expression": expression, "Result": str(result)}
    count += 1
    with open("history.json", "w") as f:
        json.dump(history, f)

# Function to display the history
def show_history():
    history_window = ctk.CTkToplevel(root)
    history_window.title("History")
    history_text = ctk.CTkTextbox(history_window, width=300, height=300)
    history_text.pack(padx=10, pady=10)
    if history:
        for key, value in history.items():
            history_text.insert(tk.END, f"{key}: {value['Expression']} = {value['Result']}\n")
    else:
        history_text.insert(tk.END, "No history available.")

# Function to reset the last history entry
def reset_last_entry():
    if history:
        last_key = list(history.keys())[-1]  # Get the last operation key
        del history[last_key]  # Remove the last operation
        with open("history.json", "w") as f:
            json.dump(history, f)
        show_history()

# Function to delete the last character in the expression
def delete_last_character():
    current = entry_var.get()
    entry_var.set(current[:-1])  # Remove the last character

# Function to delete the entire history
def delete_history():
    global history
    history = {}
    with open("history.json", "w") as f:
        json.dump(history, f)
    show_history()

# Function to add an opening parenthesis
def add_open_parenthesis():
    current = entry_var.get()
    entry_var.set(current + "(")

# Function to add a closing parenthesis
def add_close_parenthesis():
    current = entry_var.get()
    entry_var.set(current + ")")

# Initialize the main window
root = ctk.CTk()
root.title("Advanced Calculator")
root.geometry("400x700")

# Entry widget for displaying the expression
entry_var = ctk.StringVar()
entry = ctk.CTkEntry(root, textvariable=entry_var, font=("Arial", 20), width=350, height=50)
entry.pack(padx=10, pady=20)

# Buttons layout for the calculator
button_frame = ctk.CTkFrame(root)
button_frame.pack(padx=10, pady=20)

buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '=', '+'),
    ('sin', 'cos', 'tan', '^'),
    ('log', 'ln', 'exp', 'pi'),
    ('clear', 'history', 'reset', 'quit'),
    ('(', ')', 'delete')
]

# Create buttons dynamically
for row in buttons:
    for button in row:
        if button == "=":
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=calculate_and_display)
        elif button == "clear":
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=clear_display)
        elif button == "history":
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=show_history)
        elif button == "reset":
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=reset_last_entry)
        elif button == "quit":
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=root.quit)
        elif button == "delete":
            btn = ctk.CTkButton(button_frame, text="Delete", width=80, height=40, command=delete_last_character)
        elif button == "(":
            btn = ctk.CTkButton(button_frame, text="(", width=80, height=40, command=add_open_parenthesis)
        elif button == ")":
            btn = ctk.CTkButton(button_frame, text=")", width=80, height=40, command=add_close_parenthesis)
        else:
            btn = ctk.CTkButton(button_frame, text=button, width=80, height=40, command=lambda value=button: append_to_display(value))
        
        btn.grid(row=buttons.index(row), column=row.index(button), padx=5, pady=5)

# Add Clear History button
btn_clear_history = ctk.CTkButton(button_frame, text="Clear History", width=80, height=40, command=delete_history)
btn_clear_history.grid(row=len(buttons), column=0, columnspan=4, padx=5, pady=5)

# Load history from file if it exists
try:
    with open("history.json", "r") as f:
        history = json.load(f)
    reset_history = history.copy()
    count = len(history) + 1
except (FileNotFoundError, json.JSONDecodeError):
    history = {}
    reset_history = {}

# Start the main event loop
root.mainloop()
