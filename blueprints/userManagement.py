#### imports ####
from flask import Blueprint, request, render_template
from database.database import add_new_swimmer,                                                              check_existing_swimmer


# Create Blueprint for User account creation and login
userManagement_bp = Blueprint("userManagement", __name__, template_folder='../templates')


# user login handler
# ------------------
@userManagement_bp.route("/login", methods=['GET', 'POST'])
def login():   

    if request.method == 'POST':
        
        # Read data from the form if method is POST - data is submitted
        se_id = request.form.get('SE_ID')
        email = request.form.get('email')
        password = request.form.get('password')

        # Reject blank input
        if se_id.strip() == '' or email.strip() == '' or password.strip() == '':   
            return "Complete all required fields"
        
        else:
            # Valid input - check login credentials
            return f"Checking credentials for Swim England ID {se_id}"

    # or assuming first-time form visit - load login form
    else:
        return render_template('login.html')
    

# createAccount handler
# ---------------------
@userManagement_bp.route("/createAccount", methods=['GET', 'POST'])
def createAccount():   
    
    if request.method == 'POST':

        # Read data from the form if method is POST - data is submitted
        rankings_ID = int(request.form.get('SE_ID'))
        name = str(request.form.get('name'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        repassword = str(request.form.get('repassword'))
        


        #initially sets up a blank error message
        message = ""


        #checks for blank rankings_ID
        if rankings_ID == "":
            message = message + "Please enter your Swim England ID"

        #checks for invalid rankings_ID length
        elif len(str(rankings_ID)) >= 11 or len(str(rankings_ID)) <= 3:
            message = message + "Invalid ID - Please try again"

        #checks for blank email
        elif email == "":
            message = message + "Please enter an email address"

        #checks for invalid email length
        elif len(email) <= 4:
            message = message + "Username is too short - must be at least 5 characters"

        #checks for blank password
        elif password == "":
            message = message + "Please create a password"

        #checks for invalid password length
        elif len(password) <= 8:
            message = message + "Password is too short - must be at least 9 characters long"

        #checks that password includes a number
        elif not any(char.isdigit() for char in password):
            message = message + "Password must include a number"

        #checks that password includes an uppercase and lowercase letter
        elif not any(char.isupper() for char in password):
            message = message + "Password must include an uppercase letter"
        elif not any(char.islower() for char in password):
            message = message + "Password must include a lowercase letter" 

        elif password != repassword:
            message = message + "Passwords do not match - please try again"

        #checks that password includes a special character
        elif password.isalnum():
            message = message + "Password must include a special character (e.g. !, @, #, $, &, *, %, etc.)"

        #checks for blank name
        elif name == "":
            message = message + "Please enter your name"
        
        #checks that no errors have been added to the message and if not
        #adds new swimmer to database by calling add_new_swimmer function
        if message == "":
            successful_add = add_new_swimmer(rankings_ID, name, email, password)
            if successful_add:
                message = f"Account created successfully for {name} with Swim England ID {rankings_ID}"
                return message
            else:
                return "Sign-up failed - please try again"
            
        else:
            return message

    # or if method is not POST, assuming first-time form visit - load login form
    else:
        return render_template("createAccount.html")