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


import userInterface

"""
    This is the main code.  This is the .py file that you run to execute and
    run/start the application.
    Students do NOT need to change this code.
"""

userInterface.start()

def start():
	"""
		logs the user in, and runs the app
	"""

	userName = userLogin.login()

	runApp(userName)


def runApp(userName):
	userName.input("/nEnter Name: ")

	# loop until user types q
	userQuit = False
	while (not userQuit):
        print("-- Welcome to Skelly's Concert --")
    userInput = input("Enter a command:") # get first character of input
    lowerInput = userInput.lower()
    firstChar = lowerInput[0:1]
        print("Type t to run tests or q to quit")
        print()

		# get first character of input


		# menu choices, use a switch-like if-elif control structure

		"""
			here students need to change and add to this code to
			handle their menu options
		"""
		# quit
		if firstChar == 'q':
			userQuit = True

		# run some tests (this is part 1 of 2)
		elif firstChar == 't':
			runTests()

		else:
			print("ERROR: " + firstChar + " is not a valid command")

	print("\n")
	print("Thank you for using the Gladys West Map App!")
	print("\n")



def storeusers(form):
    # gives data to all session variables
    session['name'] = form.name.data
    session['lastname'] = form.lastname.data

    # creates a new folder for a user to store their information in based on their email address
    path = "/Users/mod/Documents/GitHub/outdoorParkConcertApp" + session.get('name', 'lastname')
    os.mkdir(path)
    filename = path + "/info.txt"
    # stores user's info in a txt file inside their folder
    with open(filename,"w+") as f:
        f.write(session.get('name'))
        f.write(" ")
        f.write(session.get('lastname'))
        f.close()



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
