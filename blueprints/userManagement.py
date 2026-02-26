#### imports ####
from flask import Blueprint, request, render_template, flash   
from database.database import push_extracted_data, add_new_swimmer, check_existing_swimmer, check_login_credentials, get_user_info, delete_account
from markupsafe import Markup 
from dataScraping import fetch_data_login



# Create Blueprint for User account creation and login
userManagement_bp = Blueprint("userManagement", __name__, template_folder='../templates')


# user login handler
# ------------------
@userManagement_bp.route("/login", methods=['GET', 'POST'])
def login():   

    # Access global variables
    global currentSwimmer_ID, currentSwimmer_name, currentSwimmer_email

    if request.method == 'POST':
        
        # Read data from the form if method is POST - data is submitted
        rankings_ID = int(request.form.get('rankings_ID'))
        password = str(request.form.get('password'))

        # Reject blank inputs
        if str(rankings_ID).strip() == "" or password.strip() == "": 
            flash("Please complete all required fields")  
            return False
        
        # Checking login credentials
        # If credentials are incorrect, flash error message - if correct, redierct to home page
        elif check_login_credentials(rankings_ID, password) == False:
            flash("Swim England ID or password is incorrect - please try again")
            return render_template("login.html")

        elif check_login_credentials(rankings_ID, password) == True:
            
            currentSwimmer_ID = rankings_ID
            currentSwimmer_name = get_user_info(rankings_ID)[0]
            currentSwimmer_email = get_user_info(rankings_ID)[1]


            #fetching data from the rankings website and pushing it to the database
            scrapedData = fetch_data_login(currentSwimmer_ID)
            for race_ID in range(1,36):
                for stroke in scrapedData:
                    for swim in stroke:
                        push_extracted_data(currentSwimmer_ID, race_ID, swim[0], swim[1], swim[2], swim[3])


            return render_template("home.html")

    # or assuming first-time form visit - load login form
    else:
        return render_template('login.html')
    

# createAccount handler
# ---------------------
@userManagement_bp.route("/createAccount", methods=['GET', 'POST'])
def createAccount():   
    
    if request.method == 'POST':

        # Read data from the form if method is POST - data is submitted
        rankings_ID = int(request.form.get('rankings_ID'))
        name = str(request.form.get('name'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        repassword = str(request.form.get('repassword'))
        


        #initially sets up a blank error message
        message = ""


        #checks for blank rankings_ID
        if str(rankings_ID).strip() == "":
            message = message + "Please enter your Swim England ID"

        #checks for invalid rankings_ID length
        if len(str(rankings_ID)) >= 11 or len(str(rankings_ID)) <= 3:
            if message == "":
                message = message + "Invalid ID - Please try again"
            else:
                message = message + Markup("<br>Invalid ID - Please try again")

        #checks for blank email
        if email.strip() == "":
            if message == "":
                message = message + "Please enter an email address"
            else:
                message = message + Markup("<br>Please enter an email address")

        #checks for blank password
        if password.strip() == "":
            if message == "":
                message = message + "Please create a password"
            else:
                message = message + Markup("<br>Please create a password")

        #checks for invalid password length
        if len(password) <= 8:
            if message == "":
                message = message + "Password is too short - must be at least 9 characters long"
            else:
                message = message + Markup("<br>Password is too short - must be at least 9 characters long")

        #checks that password includes a number
        if not any(char.isdigit() for char in password):
            if message == "":
                message = message + "Password must include a number"
            else:
                message = message + Markup("<br>Password must include a number")

        #checks that password includes an uppercase and lowercase letter
        if not any(char.isupper() for char in password):
            if message == "":
                message = message + "Password must include an uppercase letter"
            else:
                message = message + Markup("<br>Password must include an uppercase letter")

        if not any(char.islower() for char in password):
            if message == "":
                message = message + "Password must include a lowercase letter"
            else:
                message = message + Markup("<br>Password must include a lowercase letter") 

        if password != repassword:
            if message == "":
                message = message + "Passwords do not match - please try again"
            else:
                message = message + Markup("<br>Passwords do not match - please try again")

        #checks that password includes a special character
        if password.isalnum():
            if message == "":
                message = message + "Password must include a special character (e.g. !, @, #, $, &, *, %, etc.)"
            else:
                message = message + Markup("<br>Password must include a special character (e.g. !, @, #, $, &, *, %, etc.)")

        #checks for blank name
        if name.strip() == "":
            if message == "":
                message = message + "Please enter your name"
            else:
                message = message + Markup("<br>Please enter your name")

        if check_existing_swimmer(rankings_ID, email):
            if message == "":
                message = message + "An account with this Swim England ID or email address already exists"
            else:
                message = message + Markup("<br>An account with this Swim England ID or email address already exists")
        
        #checks that no errors have been added to the message and if not
        #adds new swimmer to database by calling add_new_swimmer function
        if message == "":
            successful_add = add_new_swimmer(rankings_ID, name, email, password)
            if successful_add:
                global currentSwimmer_ID, currentSwimmer_name, currentSwimmer_email
                currentSwimmer_ID = rankings_ID
                currentSwimmer_name = name
                currentSwimmer_email = email
                return render_template("home.html")
            else:
                flash("Sign-up failed - please try again")
                return render_template("createAccount.html")
            
        else:
            flash(message)
            return render_template("createAccount.html")
        
    # or if method is not POST, assuming first-time form visit - load login form
    else:
        return render_template("createAccount.html")
    

# log out handler
# ---------------
@userManagement_bp.route("/logout", methods=['GET', 'POST'])
def logout():   
    global currentSwimmer_ID, currentSwimmer_name, currentSwimmer_email
    currentSwimmer_ID = None
    currentSwimmer_name = None
    currentSwimmer_email = None
    return render_template("login.html")


# delete account handler
# ----------------------
@userManagement_bp.route("/deleteAccount", methods=['GET', 'POST'])
def deleteAccount():
    global currentSwimmer_ID, currentSwimmer_name, currentSwimmer_email
    delete_account(currentSwimmer_ID)
    currentSwimmer_ID = None
    currentSwimmer_name = None
    currentSwimmer_email = None
    return render_template("login.html")

