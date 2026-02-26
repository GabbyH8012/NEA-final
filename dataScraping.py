#### imports ####
from bs4 import BeautifulSoup
import httpx
from database.database import find_race_from_ID



# Defining the template for the url to be scraped
urlBase = "https://www.swimmingresults.org/individualbest/personal_best_time_date.php?back=individualbest&tiref={}&mode=A&tstroke={}&tcourse={}"



# Function to find the url to be scraped based on the swimmer and race
# --------------------------------------------------------------------
def find_url(race, course, currentSwimmer_ID):
    url = urlBase.format(currentSwimmer_ID, race, course)
    return url
    


# Function to scrape data from the calculated url
# -----------------------------------------------
def extract_data(race_ID, course, race, currentSwimmer_ID):
    url = find_url(race_ID, course, currentSwimmer_ID)
    response = httpx.get(url)
    response_html = response.text
    soup = BeautifulSoup(response_html, "html.parser")
    table = soup.find("table", id="rankTable")
    if table == None:
        return []
    records = table.find_all("tr")

    #create an array to store the scraped data in a structured way
    swimmer_data_array = []

    #scraping data within every record
    for record in records:

        #finding the tme in first collumn
        times = record.find("td", class_="tdrank_right")
        if times != None:
            times = times.text.strip()

        #finding the data that the above time was achieved
        date = record.find_all("td", class_="tdrank_centre")
        if date != []:
            date = date[2].text
        else:
            date = None

        #finding the name of the competition that the time was achieved at
        compName = record.find_all("td", class_="tdrank_left")
        if compName != []:
            compName = compName[0].text
        else:        
            compName = None

        #finding the venue of the above found competition
        venue = record.find_all("td", class_="tdrank_left")
        if venue != []:
            venue = venue[1].text
        else:
            venue = None


        # adding scraped data to previously created array 
        if times != None:
            swimmer_data_array.append([compName, date, times, venue])

    return swimmer_data_array



# Function that tells the program how to refresh the times in the rankings website when a user logs in
# ----------------------------------------------------------------------------------------------------
def fetch_data_login(currentSwimmer_ID):
        
        all_data = []


        for race_ID in range(1,19):
            course = "S"
            race_name = find_race_from_ID(race_ID) 

            result_short = extract_data(race_ID, course, race_name, currentSwimmer_ID)

            if result_short != []:         
                all_data.append(result_short)


        for race_ID in range(19,36):
            course = "L"
            race_name = find_race_from_ID(race_ID)

            result_long = extract_data((race_ID - 18), course, race_name, currentSwimmer_ID)
            if result_long != []:
                all_data.append(result_long)


        result = all_data
        return result



