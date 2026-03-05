#### imports ####
from flask import Blueprint, render_template, request, session
from database.database import add_swim_to_database, find_PBs, add_goal_to_database, find_race_from_ID
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
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs, selectedRaceNames=None)

    else:
        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs, selectedRaceNames=None)



#add goal time handler
#---------------------
@manualDataEntry_bp.route("/addGoal", methods=['GET', 'POST'])
def addGoal():
    
    if request.method == 'POST':

        # Read data from the form if method is POST - data is submitted
        race_ID = int(request.form.get('race_ID'))
        course = str(request.form.get('course'))
        goal_time = str(request.form.get('goal_time'))

        #update race_ID for long course races to match database
        if course == "L":
            race_ID = race_ID + 18

        # formatting time to match format in database
        goal_time = time_format(goal_time)

        # Add the new goal time to the database
        add_goal_to_database(race_ID, goal_time)


        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs, selectedRaceNames=None)
    


# add new swim handler
# --------------------
@manualDataEntry_bp.route("/filter", methods=['GET', 'POST'])
def filter():

        # Read data from the form if method is POST - data is submitted
        race_IDs = request.form.getlist('filter_race')
        courses = request.form.getlist('filter_course')

        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])

        # If no race or course is selected, show all rows.
        if race_IDs == [] or courses == []:
            return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs, selectedRaceNames=None)

        selected_race_names = []

        # Build race IDs from selected races/courses, then map them to race names.
        for race_id in race_IDs:
            race_id_int = int(race_id)

            if "S" in courses:
                selected_race_names.append(find_race_from_ID(race_id_int))

            if "L" in courses:
                selected_race_names.append(find_race_from_ID(race_id_int + 18))

        # Remove duplicates while preserving user selection order.
        # selected_race_names = list(dict.fromkeys(selected_race_names))

        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs, selectedRaceNames=selected_race_names)





