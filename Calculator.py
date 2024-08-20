import tkinter as tk

# Основное окно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x600")
root.resizable(False, False)

# Поле для ввода/отображения
entry = tk.Entry(root, font=("Arial", 24), width=15, borderwidth=2, relief="solid", justify='right')
entry.grid(row=0, column=0, columnspan=4, pady=20)

# Глобальная переменная для хранения выражения
expression = ""

# Функции для обработки нажатий кнопок
def button_click(value):
    global expression
    expression += str(value)
    entry.delete(0, tk.END)
    entry.insert(tk.END, expression)

def clear():
    global expression
    expression = ""
    entry.delete(0, tk.END)

def calculate():
    global expression
    try:
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        expression = str(result)
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Ошибка")
        expression = ""

# Создание кнопок
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

# Добавление кнопок на окно
for (text, row, col) in buttons:
    action = lambda x=text: button_click(x) if x != '=' else calculate()
    tk.Button(root, text=text, width=10, height=3, command=action).grid(row=row, column=col)

# Кнопка очистки
tk.Button(root, text='C', width=10, height=3, command=clear).grid(row=5, column=0, columnspan=4)

root.mainloop()
