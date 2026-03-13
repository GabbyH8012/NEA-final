#### imports ####
from flask import Blueprint, render_template, request, session
from database.database import find_PBs, find_all_results_and_goal_from_ID, find_race_from_ID



# Create Blueprint for when users are manually entering data
dataAnalysis_bp = Blueprint("dataAnalysis", __name__, template_folder='../templates')



# Route for data analysis page
# ----------------------------
@dataAnalysis_bp.route("/dataAnalysis", methods=['GET', 'POST'])
def data_analysis():

    course = ["short", "long"]
    short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])

    results = []
    goals = []
    for i in range(1,36):
        race_results, race_goal = find_all_results_and_goal_from_ID(i)
        results.append(race_results)
        goals.append(race_goal)

    return render_template("dataAnalysis.html", short_PBs=short_PBs, long_PBs=long_PBs, course=course, results=results, goals=goals, line_race_ID=1, raceName="50 Freestyle", line_course="Short course")



# Filter Line graph event handler
# -------------------------------
@dataAnalysis_bp.route("/chooseDisplayedEvent_Line", methods=['GET', 'POST'])
def choose_displayed_event_line():
        
    line_race_ID = int(request.form.get('race_ID'))
    line_course = str(request.form.get('course'))

    if line_course == "L":
        line_race_ID = line_race_ID + 18
        line_course = "Long course"
    else:        
        line_course = "Short course"

    raceName = find_race_from_ID(line_race_ID)


    course = ["short", "long"]
    short_PBs, long_PBs = find_PBs(session["currentSwimmer_ID"])

    results = []
    goals = []
    for i in range(1,36):
        race_results, race_goal = find_all_results_and_goal_from_ID(i)
        results.append(race_results)
        goals.append(race_goal)

    return render_template("dataAnalysis.html", short_PBs=short_PBs, long_PBs=long_PBs, course=course, results=results, goals=goals, line_race_ID=line_race_ID, raceName=raceName, line_course=line_course)

