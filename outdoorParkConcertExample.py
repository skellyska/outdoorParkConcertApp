"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with a since all seats are available

resources:
https://github.com/mylescruz/Tiny-Concert/blob/master/Tiny_Concert/env/app.py

Menu system for guests to:
[V]iew/display available seating
An available seat is indicated with a "a" (lower case a)
An already occupied seat is indicated with a "X" (capital x)
There must be 2 social distancing seats (available seats) between each occupied seat on a row. 
> 1 row distance between each row.  Bulk tickets that are purchased can sit next to each other.
Provide 3 types of seating
Front Seat with price $80.  Rows 0 - 4
Middle Seat with price $50.  Rows 5-10
Back Seat with price $25.  Rows 11-19
[B]uy/purchase a ticket and provide receipt with  state tax of 7.25% including an additional mandatory mask fee of $5.00
When a purchase is made, ask the user for their name & email address
[S]earch by name will display the tickets purchased by a user with a specific name.
[D]isplay all purchases.  Prints all the purchases made and shows the total amount of income/money that the venue has made.
[Q]uit
Tickets can be purchased 1 at a time or in bulk.  
> For example, a user can ask to buy 15 tickets and they should be given pricing and a group of 15 tickets available for the type of ticket they wish to buy (Front, Middle, or Back)
Seats should be labelled by rows and columns in a rectangular format
Rows are indicated with numbers
Columns are indicated with letters
Your software should provide 520 seats (20 x 26) as shown in the images below.
Your software saves data seating and purchase data into a .json  file as transactions are completed. 
> When the application restarts (is quit and ran again by the user), the last saved information is loaded/restored.  So, seating and purchase information is not lost.
"""

#FLOW
#login and creating json
#display seats and availability
#load seat data for each row as arrays that store a seat's value as empty or taken

def searchByName(name):
    """
    Func: searchByName
    Desc: a function to search by name
    """

    results = ""

    print("name = " + name)

    return results

def quit():
    """
    Func: quit
    Desc: Gracefully quits
    """

    print("Thank you for using the application")

def menu():
    """
    Func: menu
    Desc: Display the menu
    """

    # present the menu
    print("---- Menu ----")
    print("[v]iew/display available seating")
    print("[b]uy/purchase a ticket")
    print("[s]earch by name")
    print("[d]isplay all purchases")
    print()
    print("[q]uit")
    print("-----------------")
    print()

def handleUserInput(userInput):
    """
    Func: handleUserInput
    Desc: handles user input and dispatches calls
    """

    if (userInput == "v"):
        seatingView()

    elif (userInput == "s"):
        name = input("Enter a name to search for:")
        searchByName(name)

    elif (userInput == "d"):
        print("library")

    elif (userInput == "q"):
        quit()

    # "default" case, if none of the other cases were satisfied
    else:
        print("No such command." + str(userInput))

def seatingView():

    n_row = 20
    n_col = 26

    # available seat
    available_seat = 'a'

    # create some available seating
    seating = []
    for r in range(n_row):
        row = []
        for c in range(n_col):
            row.append(available_seat)
        seating.append(row)

# print available seating row
    for r in range(n_row):  
        print(r+1, end="\t")
        for c in range(n_col):
            print(seating[r][c], end=" ")
        print()

def main():
    """
    Func: main
    Desc: main routine
    """

    userInput = ""
    userQuit = False
    while (not userQuit):

        menu()

        # get user input
        userInput = input("Enter a command, or q to quit:")

        # handle user input
        handleUserInput(userInput)
        
        # print/display result
        print("userInput = " + userInput)

main()
