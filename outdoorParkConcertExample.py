"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with a since all seats are available

resources:
https://github.com/mylescruz/Tiny-Concert/blob/master/Tiny_Concert/env/app.py
https://codereview.stackexchange.com/questions/198040/user-login-database-intended-for-beginners
https://stackoverflow.com/questions/41082140/seating-plan-in-python

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
import getpass
import re
import datetime
from sqlite3 import Row
from typing import Dict
import json
from typing import Union, List
from pathlib import Path


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
    print(" ")
    print("---- Menu ----")
    print("1. View/display available seating")
    print("2. Log in to account or create account")
    print("3. Search ticket holders by name")
    print("4. Display all purchases")
    print()
    print("5. Quit")
    print("-----------------")
    print()


def handleUserInput(userInput):
    """
    Func: handleUserInput
    Desc: handles user input and dispatches calls
    """

    if (userInput == "1"):
        seatingView()
    elif (userInput == "2"):
        ticketPurchase()
    elif (userInput == "3"):
        name = input("Enter a name to search for:")
        searchByName(name)
    elif (userInput == "4"):
        print("library")
    elif (userInput == "5"):
        quit()

    # "default" case, if none of the other cases were satisfied
    else:
        print("No such command." + str(userInput))

def seatingView():
    def save(sales, taken_seats):
        f = open("data.txt", "w")
        f.write(str(sales) + "\n")
        for x in taken_seats:
            f.write(x + "\n")
        f.close()
    def load():
        f = open("data.txt")
        sales = f.readline().replace("\n", "")
        taken_seats = []
        d = True
        while d == True:
            line = f.readline().replace("\n", "")
            if line == "":
                d = False
            else:
               taken_seats.append(line)
        if sales == "":
            sales = 0
        else:
            sales = int(sales)
        f.close()
        return (int(sales), taken_seats)
    def display_seats(taken_seats):
        seating = []
        xd = 0
        for xd in range(15):
            row = []
            xda = 0
            for xda in range(15):
                row.append('a')
                xda = xda + 1
            xd = xd + 1
            seating.append(row)
        for x in taken_seats:
            pos = x.split(",")
            seating[(int(pos[0]) - 1)][(int(pos[0]))] = "X"
        dx = 1
        for row in seating:
            if len(str(dx)) == 1:
                de = " " + str(dx) + "   "
            elif len(str(dx)) == 2:
                de = " " + str(dx) + "  "
            else:
                de = dx
            print ("Row: " + str(de) + " ".join(row))
            dx = dx + 1
    def list_options():
        print(" ")
        print ("1: View current seating")
        print ("2: View price per row")
        print ("3: View sales")
        print ("4: Buy ticket")
        print (" ")
        print("5. Quit")
        new_input = input("Your choice: ")
        return (new_input)
    def purchase_seat(taken_seats):
        print ("Would you like to view current seating availability? ")
        print ("'1' = yes, '2' = no")
        newinput = input("? ")
        if newinput == "1":
           display_seats(taken_seats)
        x = True
        while x == True:
            cost = 0
            print ("what row would you like to buy a seat on? ")
            rowx = input("What row? ")
            print ("What seat would you like to purchase?")
            rowy = input("what seat? ")
            d = (str(rowx) + "," + str(rowy))
            h = 0
            for x in taken_seats:
                if d == x:
                    h = 1
            if h == 1:
               print ("That seat is already taken, please choose another seat.")
            elif int(rowx) > 15 or int(rowy) > 15:
                print ("Invalid seating location, please choose another seat.")
            else:
                print ("seat purchased.")
                cost = (200 - (10 * int(rowx)))
                x = False
        return (cost, (str(rowx) + "," + str(rowy)))
    da = load()
    sales = da[0]
    taken_seats = da[1]
    quitter = 0
    while quitter == 0:
        new_input = list_options()
        if new_input == "5":
            save(sales, taken_seats)
            quitter = 1
        elif new_input == "4":
            g = True
            while g == True:
                new_seat = purchase_seat(taken_seats)
                taken_seats.append(new_seat[1])
                print ("That will be: $ " + str(new_seat[0]))
                sales = sales + new_seat[0]
                print ("Would you like to purchase another seat?")
                new_input = input("'1' = yes, '2' = no: ")
                if new_input == "1":
                    pass
                else:
                    g = False
        elif new_input == "3":
            print ("Total sales: $" + str(sales))
        elif new_input == "2":
            xd = 0
            while xd < 15:
                print ("Row " + str(xd + 1) + ": is $" + str((200 - (10 * xd)) - 10))
                xd = xd + 1
        elif new_input == "1":
            display_seats(taken_seats)
        else:
            print("Invalid option.")


def ticketPurchase():
    print("\n\nTicket Booking System\n")
    restart = ("Y")

    while restart != ("n", "NO", "no", "N"):
        print("1. Ticket Prices")
        print("2. Buy a ticket")
        print("3. Register new user or Login")
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
            DEFAULT_FILE_PATH = '/Users/carleelyons/Desktop/Eric Coding Bullshit/Github repos/outdoorParkConcertApp/users/users.json'

            def create_file_if_not_exists(file_path: str) -> None:
                Path(file_path).touch()
            def get_json_file_contents(file_path: str) -> Union[List, None]:
                try:
                    json_file = open(file_path)
                except IOError:
                    return None
                try:
                    file_contents = json.load(json_file)
                except ValueError:
                    file_contents = None
                json_file.close()
                return file_contents


            def prepare_new_user_data(username: str, password: str) -> Dict:
                new_user = {
                    'username': username,
                    'password': password,
                    'created': str(datetime.datetime.now()),
                    'active': True
                }
            def check_if_user_already_exists(username: str, json_file_path: str=DEFAULT_FILE_PATH) -> bool:
                all_users = get_json_file_contents(json_file_path)
                if not all_users:
                    return False
                for user in all_users:
                    if user['username'] == username:
                        return True
                return False
            def retrieve_user(username: str, json_filepath: str=DEFAULT_FILE_PATH) -> Union[Dict, None]:
                all_users = get_json_file_contents(json_filepath)
                for user in all_users:
                    if user['username'] == username:
                        return user
                return None
            def authenticate_username_and_password(username: str, password: str) -> bool:
                user = retrieve_user(username)
                check_password = user['password']
                if not user:
                    return False
                if not check_password(password):
                    return False
                return True
            
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
                    user_added_successfully = try_adding_user(username, password)
            
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
            def prepare_new_user_data(username: str, password: str) -> Dict:
                new_user = {
                    'username': username,
                    'password': password,
                    'created': str(datetime.datetime.now()),
                    'active': True
                }
                return new_user
            def check_if_user_already_exists(username: str, json_file_path: str=DEFAULT_FILE_PATH) -> bool:
                all_users = get_json_file_contents(json_file_path)
                if not all_users:
                    return False
                for user in all_users:
                    if user['username'] == username:
                        return True
            def add_user(username: str, password: str, json_file_path: str=DEFAULT_FILE_PATH) -> None:
                create_file_if_not_exists(json_file_path)
                is_duplicate_user = check_if_user_already_exists(username, json_file_path)
                if is_duplicate_user:
                    raise ValueError(f'Username "{username}" already exists.')
                new_user = prepare_new_user_data(username, password)
                all_users = get_json_file_contents(json_file_path)
                if not all_users:
                    all_users = []
                all_users.append(new_user)
                with open(json_file_path, 'w') as users_file:
                    json.dump(all_users, users_file, indent=2)
            

        user_menu()


main()
