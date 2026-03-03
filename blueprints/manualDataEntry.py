#### imports ####
from flask import Blueprint, render_template, request, session
from database.database import add_swim_to_database, find_PBs
from dataScraping import date_format, time_format



# Create Blueprint for when users are manually entering data
manualDataEntry_bp = Blueprint("manualDataEntry", __name__, template_folder='../templates')



# add new swim handler
# --------------------
@manualDataEntry_bp.route("/addSwim", methods=['GET', 'POST'])
def addSwim():
    
    if request.method == 'POST':

        # Read data from the form if method is POST - data is submitted
        race_ID = int(request.form.get('race_ID'))
        course = str(request.form.get('course'))
        comp_name = str(request.form.get('comp_name'))
        date = str(request.form.get('date'))
        final_time = str(request.form.get('final_time'))
        goal_time = str(request.form.get('goal_time'))

        #update race_ID for long course races to match database
        if course == "L":
            race_ID = race_ID + 18
            
        # formatting date to match format in database
        date = date_format(date)

        # formatting time to match format in database
        final_time = time_format(final_time)

        # Add the new swim to the database
        add_swim_to_database(race_ID, comp_name, date, final_time, goal_time)
    
        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs)



    else:
        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs)



