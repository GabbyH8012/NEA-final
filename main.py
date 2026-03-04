#### imports ####
from genericpath import isfile
from flask import Flask, redirect
from blueprints.userManagement import userManagement_bp
from blueprints.manualDataEntry import manualDataEntry_bp
from database.database import createTables, populate_race_table



# Create flask application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages to the user + sessions


# Register blueprints
app.register_blueprint(userManagement_bp)                        
app.register_blueprint(manualDataEntry_bp)

# check if database tables exist and create if not
if isfile("database/swimmer_info.db") == False:
    createTables() 
    populate_race_table()


# Handle default "/" landing page route
@app.route('/')
def landing():   
    return redirect("/login")


# Launch the application
if __name__ == '__main__':
    app.run(debug=True)



