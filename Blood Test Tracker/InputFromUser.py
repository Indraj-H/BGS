name = input("Please enter your name: ") # Here we create a variable called name which asks for the name of the user
colour = input("Please enter red, green or blue: ") # Here we create a variable called colour which asks for the users fav colour and makes the name the entered colour

if colour == "red":
    print("Hello\033[31m " + name + "!\033[0m Welcome to the program.")

elif colour == "green":
    print("Hello\033[32m " + name + "!\033[0m Welcome to the program.")

elif colour == "blue":
    print("Hello\033[34m " + name + "!\033[0m Welcome to the program.")