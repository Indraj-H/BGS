import time

name = input("Please enter your name: ") # Here we create a variable called name which asks for the name of the user
code = 1

while True:
    print(f"\033[{code}m{code}: {name}\033[0m")
    time.sleep(1)
    code += 1


