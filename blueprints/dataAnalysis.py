#### imports ####
from flask import Blueprint, render_template, session
from database.database import find_PBs, find_all_results_and_goal_from_ID



# Create Blueprint for when users are manually entering data
dataAnalysis_bp = Blueprint("dataAnalysis", __name__, template_folder='../templates')



# add new swim handler
# --------------------
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

    

    return render_template("dataAnalysis.html", short_PBs=short_PBs, long_PBs=long_PBs, course=course, results=results, goals=goals)




