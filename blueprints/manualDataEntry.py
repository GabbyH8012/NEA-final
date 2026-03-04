#### imports ####
from flask import Blueprint, render_template, request, session
from database.database import add_swim_to_database, find_PBs, add_goal_to_database, find_PB_from_ID
from dataScraping import date_format, time_format
from datetime import datetime




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


        # drop = str(calculate_drop(goal_time, race_ID))
        # drop = time_format(drop)

        short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])
        return render_template("home.html", short_PBs=short_PBs, long_PBs=long_PBs,)
    


# # Function to calculated the required time drop to achieve the goal time from PB
# # ------------------------------------------------------------------------------
# def calculate_drop(goal_time, race_ID):
#     pb = find_PB_from_ID(race_ID)
#     if pb is None:
#         return None

#     def parse_swim_time(value):
#         for fmt in ("%M:%S.%f", "%M:%S"):
#             try:
#                 return datetime.strptime(value, fmt)
#             except ValueError:
#                 continue
#         raise ValueError(f"Invalid time format: {value}")

#     pb_time = parse_swim_time(pb)
#     goal_time_parsed = parse_swim_time(goal_time)
#     drop = pb_time - goal_time_parsed
#     return drop



# # Function to calculated the required time drop per length to achieve the goal time from PB
# # -----------------------------------------------------------------------------------------
# def calculate_drop_per_length(goal_time, race_ID):
#     drop = calculate_drop(goal_time, race_ID)

  


