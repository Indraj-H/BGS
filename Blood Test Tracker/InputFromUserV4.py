from openpyxl import Workbook # To install this type - "Working Directory Path" -m pip install openpyxl
import time

# Title
print("Welcome Indy's Data Collector")
time.sleep(1)
print()

# Excel Workbook Initialization
workbook = Workbook()
sheet = workbook.active

# Variables
name1 = input("Please enter person 1 full name: ") # Here we create a variable called firstname which asks for the name of the user
name2 = input("Please enter person 2 full name: ")
name3 = input("Please enter person 3 full name: ")

sheet.cell(row=1, column=1).value = "Name"
sheet.cell(row=2, column=1).value = name1
sheet.cell(row=3, column=1).value = name2
sheet.cell(row=4, column=1).value = name3

workbook.save("names.xlsx")

# Variable Displayed
print("\033[32m" "Data Collected Successfully!" "\033[0m")
