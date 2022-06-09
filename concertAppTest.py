from flask import Flask, flash, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from concerts import *
import os.path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'foo'

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

dateSelected = "None"
dataA = []
dataB = []
dataC = []
dataD = []
dataE = []

# Registration form: allows user to register for the website
class RegisterForm(FlaskForm):
    name = StringField('First Name:', validators=[DataRequired()])
    lastname = StringField('Last Name:', validators=[DataRequired()])
    emailaddress = StringField('Email:', validators=[DataRequired()])
    password = StringField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')

# Login form: allows user to login into website to access their information and check reservations
class LoginForm(FlaskForm):
    emailadd = StringField('Email:', validators=[DataRequired()])
    pword = PasswordField('Password: ', validators=[DataRequired()])
    login = SubmitField('Login')

# Cancel reservation form: allows user to cancel any current reservations
class ConfirmationForm(FlaskForm):
    pw = PasswordField('Password: ', validators=[DataRequired()])
    confirm = SubmitField('Confirm')

# index page
@app.route("/", methods = ['GET'])
def index():
    return render_template('index.html', name=session.get('name'))

# allows user to login to their account
@app.route("/login", methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # checks if a user has a registered email address
        filename = "data/users/" + loginform.emailadd.data + "/" + "info.txt"
        try:
            open(filename)
        except IOError:
            # if user does not have a registered email, redirects them back to login to create a new account
            flash('Email address not found. Please register to make a new account','error') # flashes error message for next page being directed to
            return redirect(url_for('login'))
        
        # opens user's info file and takes in the data
        with open(filename,"r") as f:
            line = f.readline()
            current = line.split() # splits current into an array of values
            infoInput = loginform.emailadd.data + loginform.pword.data
            # a user must input correct email address and password to login
            if infoInput == current[0] + current[1]:
                # if login successful, user's info is stored in current session
                session['emailaddress'] = current[0]
                session['password'] = current[1]
                session['name'] = current[2]
                session['lastname'] = current[3]
                flash('Logged in successfully!','info') # flashes confirmation message for next page being directed to
                return redirect(url_for('concerts')) # redirects logged in user to concerts 
            else:
                flash('Wrong information inputted. Please try again to login!','error') # flashes error message for next page being directed to
                return redirect(url_for('login'))

    return render_template('login.html', loginform = loginform, name=session.get('name'))  

# allows user to register for an account if new to the site
@app.route("/register", methods=['GET','POST'])
def register():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        direc = "data/users/" + registerform.emailaddress.data
        # checks if the email address entered is already registered in the system
        isdir = os.path.isdir(direc)  
        if isdir: 
            # if there is a file with that email, redirects them to login page
            flash('The email address you entered is already registered','error') # flashes error message for next page being directed to
            return redirect(url_for('login'))
        else:
            # if there is no file with that email, stores user in the system
            storeusers(registerform)
            flash('Registered successfully!','info') # flashes confirmation message for next page being directed to
            return redirect(url_for('concerts'))
    
    return render_template('register.html', registerform=registerform)

# function to create a folder for each new user who registers for the site
# stores their first name, last name, email addresss and password
def storeusers(form):
    # gives data to all session variables
    session['name'] = form.name.data
    session['lastname'] = form.lastname.data
    session['emailaddress'] = form.emailaddress.data
    session['password'] = form.password.data

    # creates a new folder for a user to store their information in based on their email address
    path = "data/users/" + session.get('emailaddress')
    os.mkdir(path)
    filename = path + "/info.txt"
    # stores user's info in a txt file inside their folder
    with open(filename,"w+") as f:
        f.write(session.get('emailaddress'))
        f.write(" ")
        f.write(session.get('password'))
        f.write(" ")
        f.write(session.get('name'))
        f.write(" ")
        f.write(session.get('lastname'))
        f.close()

# logs user out of website by clearing all session data           
@app.route("/logout", methods=['GET','POST'])
def logout():
    session.pop('name', None)
    session.pop('lastname', None)
    session.pop('emailaddress', None)
    session.pop('password', None)
    session.pop('seat', None)
    session.pop('date', None)
    flash("Logout successful!") # flashes confirmation message for next page being directed to
    return redirect(url_for('login'))

# displays the current concerts offered in the series
@app.route("/concerts")
def concerts():
    concerts = Concerts()
    M = []  # array that stores the Musicians
    D = []  # array that stores the Dates
    Date = [] # array that stores the Dates without the "_"

    # populates the M, D, and Dates arrays
    # key: stores the date
    # value: stores the musician
    for key, value in concerts.concertsDict.items():
        M.append(value)
        D.append(key)
        Date.append(key)

    i = 0
    for x in Date:
        Date[i] = Date[i].replace("_", " ") # replaces "_" with a space for a cleaner look for the date
        i = i + 1

    return render_template('concerts.html', M = M, D = D, Date = Date, name=session.get('name'))

# page that confirms the concert selected from the 'Concerts' page
@app.route("/concertselected", methods=['GET','POST'])
def concertselected():
    dateSelected = request.args.get('date') # uses the date selected by user to determine which concert seats to view

    session['date'] = dateSelected
    session['seat'] = ""
    
    date = ""
    date = dateSelected.replace("_"," ") # replaces "_" with a space for a cleaner look for the date

    # checks if a user is logged in and checks if the user has a reservation for the concert selected
    if session.get('emailadress'):
        filename = "data/users/" + session.get('emailaddress') + "/" + date + ".txt"
        try:
            open(filename)
            with open(filename,"r") as f:
                session['seat'] = f.readline()
                f.close()
        except IOError:
            session['seat'] = ""

    # gives the musician session variable a value to display for the user 
    concerts = Concerts()
    for key, value in concerts.concertsDict.items():
        if key == dateSelected:
            session['musician'] = value

    return render_template('concertselected.html', name=session.get('name'), date = date, musician = session.get('musician'))

# displays the a concert's seats and their availability
@app.route("/seatview", methods = ['GET'])
def seatview():
    global dataA
    global dataB
    global dataC
    global dataD
    global dataE

    if session.get('date') is None:
        flash('Must select a concert to view seats','error') # flashes error message for next page being directed to
        return redirect(url_for('concerts'))

    loadSeats() # loads the seats' data for each row
    # arrays that store a seat's value for empty or taken
    iconA = []
    iconB = []
    iconC = []
    iconD = []
    iconE = []
    reservedSeat = "" 
    reservedIcon = "/static/occupied.png"
    availableIcon = "/static/empty.png"
    
    # sets up the occupied or empty icon for each seat in each row
    setupRowIconsAndSeats(iconA,dataA)
    setupRowIconsAndSeats(iconB,dataB)
    setupRowIconsAndSeats(iconC,dataC)
    setupRowIconsAndSeats(iconD,dataD)
    setupRowIconsAndSeats(iconE,dataE)
    
    # if the user is logged in, it shows the user's current seats for that given concert
    if session.get('emailaddress'):
        filename = "data/users/" + session.get('emailaddress') + "/" + session.get('date') + ".txt"
        try:
            open(filename)
            with open(filename,"r") as f:
                line = f.readline()
                reservedSeat = line
                f.close()
        except IOError: # if file does not exist, user does not have a reserved seat for that concert
            reservedSeat = ""

    date = session.get('date').replace("_"," ") # replaces "_" with a space for a cleaner look for the date

    return render_template('seatview.html', reserved = reservedIcon, available = availableIcon, A = iconA, B = iconB, C = iconC, D = iconD, E = iconE, seat=reservedSeat, musician = session.get('musician'), date = date, name=session.get('name'))

# determines which row and seat was selected and allocates the data
@app.route("/seatselect", methods=['GET','POST'])
def seatselect():

    if session.get('name') is None: # if there is no user logged in
        flash('Must login to reserve a seat','error') # flashes error message for next page being directed to
        return redirect(url_for('login'))

    global dataA
    global dataB
    global dataC
    global dataD
    global dataE
    
    loadSeats()
    row = request.args.get('row') # row is taken from the seat icon selected
    seat = request.args.get('seat') # seat is taken from teh seat icon selected
    seatNum = int(seat) # turns seat variable into an int
    dateSelected = session.get('date') # date is taken from the current session

    # checks which row was selected
    # if the selected seat's value is "None", the users information is stored in that seat using 'reserveSeat' function
    # if the selected seat's value is anything else, the seat is taken and the user is redirected back to seat view with an error message
    if(row == "A"):
        if dataA[seatNum] == "None":
            dataA = reserveSeat("A", dataA, seatNum, dateSelected)
        else:
            flash('This seat is already reserved', 'error') # flashes error message for next page being directed to
            return redirect(url_for('seatview'))
    if(row == "B"):
        if dataB[seatNum] == "None":
            dataB = reserveSeat("B", dataB, seatNum, dateSelected)
        else:
            flash('This seat is already reserved', 'error') # flashes error message for next page being directed to
            return redirect(url_for('seatview'))
    if(row == "C"):
        if dataC[seatNum] == "None":
            dataC = reserveSeat("C", dataC, seatNum, dateSelected)
        else:
            flash('This seat is already reserved', 'error') # flashes error message for next page being directed to
            return redirect(url_for('seatview'))
    if(row == "D"):
        if dataD[seatNum] == "None":
            dataD = reserveSeat("D", dataD, seatNum, dateSelected)
        else:
            flash('This seat is already reserved', 'error') # flashes error message for next page being directed to
            return redirect(url_for('seatview'))
    if(row == "E"):
        if dataE[seatNum] == "None":
            dataE = reserveSeat("E", dataE, seatNum, dateSelected)
        else:
            flash('This seat is already reserved', 'error') # flashes error message for next page being directed to
            return redirect(url_for('seatview'))

    return render_template('seatselect.html', name=session.get('name'), row = row, seat = seatNum + 1)

# displays a user's current reservations and allows the ability to cancel a reservation
@app.route("/reservation", methods = ['GET','POST'])
def reservation():
    if session.get('name') is None: # a user must login to view their current reservations
        flash('Must login to see your reservation') # flashes error message for next page being directed to
        return redirect(url_for('login'))
    
    concerts = Concerts()
    seats = []
    dates = []
    d = []
    i = 0
    # for loop to populate the seats and dates arrays for a user to see current reservations
    for key, value in concerts.concertsDict.items():
        filename = "data/users/" + session.get('emailaddress') + "/" + key + ".txt"
        try:
            open(filename)
            with open(filename,"r") as f:
                line = f.readline()
                seats.append(line) # populates the seats array with reserved seats 
                dates.append(key) # populates the dates array with reserved concerts
                i = i + 1
                f.close()
        except IOError: # if user has no reservation for certain date, then skips
            pass

    j = 0
    for x in dates:
        temp = dates[j].replace("_"," ") # replaces "_" with a space for a cleaner look for the date
        d.append(temp)
        j += 1

    return render_template('reservation.html', name = session.get('name'), seats = seats, dates = dates, len = len(dates), d = d)

# confirmation page to cancel a reservation
@app.route("/cancelreservation", methods = ['GET', 'POST'])
def cancelreservation():
    dateCancel = request.args.get('temp') # takes in date selected to cancel the reservation
    form = ConfirmationForm()
    if form.validate_on_submit():
        if (session.get('password') == form.pw.data):   # a user must re-enter their password to confirm cancellation
            cancelAnyReservationForUser(dateCancel)
            flash('Reservation cancelled','info') # flashes confirmation message for next page being directed to
            return redirect(url_for('reservation'))
        else:
            flash('Wrong information inputted. Please try again to cancel the reservation.', 'error') # flashes error message for next page being directed to
            return redirect(url_for('cancelreservation'))
    return render_template('cancelreservation.html', form = form, name=session.get('name'))

# reserves a seat for a user
# takes in the row selected, the rows current values, the seat number selected and the current date
def reserveSeat(row, data, seatNum, date):
    filename = "data/concerts/" + date + "/" + row + ".txt" # file's name based on date and row of the concert 
    # a user's first and last name is now stored in the current seat chosen
    data[seatNum] = session.get('name')+session.get('lastname') 
    selectedSeat = row + str(seatNum + 1) # gives the real value of the seat number a user chose
    # seatfile: gives the txt file that will be stored in a user's folder
    seatfile = "data/users/" + session.get('emailaddress') + "/" + session.get('date') + ".txt" 

    if session.get('seat') is None: # if a user has no current seats at that date, creates new file and writes to it
        session['seat'] = selectedSeat
        with open(seatfile,"w") as f:
            f.write(selectedSeat)
            f.close()
    else: # if a user already has seats reserved, concatenate new seat with previous seats
        session['seat'] += (" " + selectedSeat)
        with open(seatfile,"a") as f:
            f.write(" ")
            f.write(selectedSeat)
            f.close()
    
    # write new data into the txt file with 
    with open(filename,"w") as f:
        f.write(data[0])
        f.write(" ")
        f.write(data[1])
        f.write(" ")
        f.write(data[2])
        f.write(" ")
        f.write(data[3])    
        f.close()
    return data

def loadSeats():
    global dataA
    global dataB
    global dataC
    global dataD
    global dataE

    # populates each row with new users info
    dataA = loadData("A",dataA)
    dataB = loadData("B",dataB)
    dataC = loadData("C",dataC)
    dataD = loadData("D",dataD)
    dataE = loadData("E",dataE)

# loads data of each seat into the row
def loadData(row, data):
    filename = "data/concerts/"+session.get('date')+"/"+row+".txt"
    with open(filename) as f:
        line = f.readline()
        data = line.split(" ") # separates data in the line by a space
    return data

# gives each seat in a row an empty or occupied value which is shown on the 'Seat View'
def setupRowIconsAndSeats(icon, data):
    for i, seatI in enumerate(data):
        if seatI == "None":
            icon.append("/static/empty.png")
        else:
            icon.append("/static/occupied.png")         

# clears the user's name from the txt file that contains the concert's seats
# dateSelected: used to get the file under a user's name to determine what seats to cancel
def cancelAnyReservationForUser(dateSelected):
    global dataA
    global dataB
    global dataC
    global dataD
    global dataE

    user = session.get('name')+session.get('lastname')            

    # checks each row to see if user has a seat reserved
    removeUser(user, dateSelected, "A", dataA)
    removeUser(user, dateSelected, "B", dataB)
    removeUser(user, dateSelected, "C", dataC)
    removeUser(user, dateSelected, "D", dataD)
    removeUser(user, dateSelected, "E", dataE)

    filename = "data/users/" + session.get('emailaddress') + "/" + dateSelected + ".txt"
    # clears the user's file with the data stored of the seat they reserved
    with open(filename,"w") as f:
        f.seek(0)
        f.truncate()
        f.close()
    os.remove(filename)

    session.pop('seat', None)

# resets the seat in the row given back to "None" which signifies an empty seat
def removeUser(user, date, row, data):
    filename = "data/concerts/" + date + "/" + row + ".txt" #open each row on that day
    with open(filename,"r+") as f:
        line = f.readline()                           
        data = line.split(" ")  
        newData = data

        for i, currentSeat in enumerate(data):
            if currentSeat == user: 
                newData[i] = "None" # if name in file matches the user given, mark that seat as empty
            else:
                newData[i] = data[i] # do not touch previous name or empty seat, if not a match
        
        f.seek(0) # goes to first space in the txt file
        f.truncate() # clears file of all data
        # rewrites the data into the txt file
        f.write(newData[0]) 
        f.write(" ")
        f.write(newData[1])
        f.write(" ")
        f.write(newData[2])
        f.write(" ")
        f.write(newData[3])    
        f.close()