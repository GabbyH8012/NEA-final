#### imports ####
from genericpath import isfile
from flask import Flask, redirect
from blueprints.userManagement import userManagement_bp
from database.database import createTables
              

# Create flask application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages to the user

# Register blueprints
app.register_blueprint(userManagement_bp)                        


# check if database tables exist and create if not
if isfile("database/swimmer_info.db") == False:
    createTables()  


# Handle default "/" home page route
@app.route('/')
def home():   
    return redirect("/login")


# Launch the application
if __name__ == '__main__':
    app.run(debug=True)
