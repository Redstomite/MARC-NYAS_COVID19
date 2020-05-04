from add import Add as MARC_Add
from scan import Scan as MARC_Scan
details_list = ["First Name", "Middle Name", "Last name", "Nationality", "Gender", "Age"]
#
current_location = "JFK Int'l, USA"

print("Welcome to " + current_location)
input_list = []

add_func = MARC_Add()
scan_func = MARC_Scan()

while True:
    operation = input("Scan or Add?: ")
    if operation == "Scan":
        for output in scan_func.scan():
            print(output)

        confirm = input("Proceed with writing?(y/n): ")

        if confirm == "y":
            for output in scan_func.pin_location(current_location):
                print(output)

    else:
        add_func.flush()
        while True:
            operation = input("Load, Check, Add, or Flush?(b to break):  ")

            if operation == "Load":
                details = []

                for i in details_list:
                    new_detail = input("Enter " + i + ":  ")
                    details.append(new_detail)
                details.append(current_location)
                print(details)

                output = add_func.load(details, current_location)
                print(output)

            if operation == "Check":
                for output in add_func.check():
                    print(output)

            if operation == "Add":
                confirm = input("Do you really want to add?(yes/no):  ")
                if confirm == "yes":
                    for output in add_func.user_add():
                        print(output)

            if operation == "Flush":
                add_func.flush()

            if operation == "b":
                break
