"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with a since all seats are available

resources:
https://github.com/mylescruz/Tiny-Concert/blob/master/Tiny_Concert/env/app.py
https://codereview.stackexchange.com/questions/198040/user-login-database-intended-for-beginners

Menu system for guests to:
[V]iew/display available seating
An available seat is indicated with a "a" (lower case a)
An already occupied seat is indicated with a "X" (capital x)
Provide 3 types of seating
Front Seat with price $80.  Rows 0 - 4
Middle Seat with price $50.  Rows 5-10
Back Seat with price $25.  Rows 11-19
[B]uy/purchase a ticket and provide receipt with  state tax of 7.25%
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

# FLOW
# login and creating json
# display seats and availability
# load seat data for each row as arrays that store a seat's value as empty or taken


from distutils.log import error
import os
import getpass
import re


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
    elif (userInput == "b"):
        ticketPurchase()
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


def ticketPurchase():
    print("\n\nTicket Booking System\n")
    restart = ("Y")

    while restart != ("n", "NO", "no", "N"):
        print("1. Check Ticket Prices")
        print("2. Ticket Reservation")
        print("3. Register new user")
        option = int(input("\nEnter your option: "))
        if option == 1:
            print("Front Seat with price $80.  Rows 0 - 4")
            print("Middle Seat with price $50.  Rows 5-10")
            print("Back Seat with price $25.  Rows 11-19")
            ticketPurchase()
        elif option == 2:
            people = int(
                input("\nEnter number of tickets you would like to purchase: "))
            name_l = []
            age_l = []
            for p in range(people):
                name = str(input("\nName :"))
                name_l.append(name)
                age = int(input("\nAge: "))
                age_l.append(age)
                restart = str(
                    input("\nWould you like to purchase anymore tickets? y/n:"))
                if restart in ("y", "YES", "yes", "Y"):
                    restart = ("Y")
                else:
                    x = 0
            print("\n Total Ticket: ", people)
            for p in range(1, people+1):
                print("Ticket:", p)
                print("Name: ", name_l)
                print("Age: ", age_l)
                x += 1
        elif option == 3:
            def user_menu():
                menu = "\n".join([
                    'Select an option by entering its number and pressing Enter.',
                    '1. Create a user account',
                    '2. Log in to existing account',
                ])
                print(menu)
                valid_selections = [1, 2]
                input_is_valid = False
                selection = None
                while not input_is_valid:
                    try:
                        selection = int(input('Selection: '))
                        if selection in valid_selections:
                            input_is_valid = True
                        else:
                            print(
                                'The number you have entered is not a valid selection')
                    except ValueError:
                        print('The value you entered is not a number.')
                handle_main_menu_selection(selection)

            def handle_main_menu_selection(selection: int):
                if selection == 1:
                    create_new_user_menu()
                elif selection == 2:
                    user_login_menu()
                else:
                    raise ValueError(f'Selection {selection} is invalid.')

            def create_new_user_menu():
                menu = '\n'.join([
                    '---'
                    'Account creation',
                    'Username must...',
                    '\t- be at least 3 characters long',
                    '\t- contain only letters, numbers, and underscores',
                    'Password must...',
                    '\t- be at least 8 characters long',
                    '---'
                ])
                print(menu)
                user_added_successfully = False
                username = ''
                while not user_added_successfully:
                
                    username = get_username_input()
                    password = get_password_input()
                    user_added_successfully = try_adding_user(
                            username, password)
                    if not user_added_successfully:
                            print(f'Username "{username}" already exists.')
                    else:
                        raise ValueError(str(error))
            def try_adding_user(username: str, password: str) -> bool:
                """
                Attempts to add a user to the user database file.
                :param username: The username provided by the user.
                :param password: The password provided to the user,in clear text.
                :return: Whether the user was added succesfully.
                """
                try:
                    add_user(username, password)
                    return True
                except ValueError:
                    return False
            def user_login_menu() -> None:
                menu = '\n'.join([
                   '---',
                   'User login',
                   '---'
                ])
                print(menu)
                login_successful = False
                while not login_successful:
                    username = get_username_input()
                    password = get_password_input()
                    login_successful = authenticate_username_and_password(username, password)
                    if not login_successful:
                        print('Incorrect username or password.')
                    print('Login successful.')
            def get_username_input() -> str:
                """
                Request username input from the user.
                :return: The username entered by the user.
                """
                minimum_length = 3
                username = input('Enter username: ')
                if len(username) < minimum_length:
                    raise ValueError('Username must be at least 3 characters.')
                # match upper & lower case letters, numbers, and underscores
                pattern = re.compile('^([a-zA-Z0-9_]+)$')
                if not pattern.match(username):
                    raise ValueError('Username must consist of only letters, numbers, and underscores.')
                return username
            def get_password_input() -> str:
                """
                Request password input from the user.
                :return: The password entered by the user.
                """
                minimum_length = 8
                password = getpass.getpass('Enter password: ')
                if len(password) < minimum_length:
                    raise ValueError('Password must be at least 8 characters.')
                return password
        user_menu()



def storeusers(form):
    session = []
    # gives data to all session variables
    session['name'] = form.name.data
    session['lastname'] = form.lastname.data

    # creates a new folder for a user to store their information in based on their email address
    path = "/Users/mod/Documents/Github/outdoorParkConcertApp" + \
        session.get('name', 'lastname')
    os.mkdir(path)
    filename = path + "/info.txt"
    # stores user's info in a txt file inside their folder
    with open(filename, "w+") as f:
        f.write(session.get('name'))
        f.write(" ")
        f.write(session.get('lastname'))
        f.close()


main()
