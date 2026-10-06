import tkinter as tk

# Functions
def click(event):
    global expression
    expression += str(event.widget.cget("text"))
    entry_var.set(expression)

def clear():
    global expression
    expression = ""
    entry_var.set("")

def calculate():
    global expression
    try:
        result = str(eval(expression))
        entry_var.set(result)
        expression = result
    except Exception:
        entry_var.set("Error")
        expression = ""

# Main window
root = tk.Tk()
root.title("Calculator")
root.geometry("500x600")

expression = ""
entry_var = tk.StringVar()

# Entry box
entry = tk.Entry(root, textvar=entry_var, font=("Arial", 24), bd=5, relief=tk.RIDGE, justify="right")
entry.pack(fill="both", ipadx=8, pady=10, padx=10)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack()

# Buttons
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for i in range(4):
    for j in range(4):
        btn = tk.Button(button_frame, text=buttons[i][j], font=("Arial", 20), height=2, width=5, bd=3)
        btn.grid(row=i, column=j, padx=5, pady=5)
        if buttons[i][j] == "=":
            btn.bind("<Button-1>", lambda e: calculate())
        else:
            btn.bind("<Button-1>", click)

# Clear button
clear_btn = tk.Button(root, text="C", font=("Arial", 20), height=2, width=22, bd=3, command=clear)
clear_btn.pack(pady=10)

# Run the app
root.mainloop()
