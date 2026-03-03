#### imports ####
from bs4 import BeautifulSoup
import httpx
from flask import session



# Defining the template for the url to be scraped
urlBase = "https://www.swimmingresults.org/individualbest/personal_best_time_date.php?back=individualbest&tiref={}&mode=A&tstroke={}&tcourse={}"



# Function to find the url to be scraped based on the swimmer and race
# --------------------------------------------------------------------
def find_url(race, course):
    url = urlBase.format(session["currentSwimmer_ID"], race, course)
    return url
    


# Function to scrape data from the calculated url
# -----------------------------------------------
def extract_data(race_ID_num, course, race_ID):
    url = find_url(race_ID_num, course)
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
            times = time_format(times)


        #finding the data that the above time was achieved
        date = record.find_all("td", class_="tdrank_centre")
        if date != []:
            date = date[2].text
            date = date_format(date)
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
            swimmer_data_array.append([race_ID, compName, date, times, venue])

    return swimmer_data_array



# Function that tells the program how to refresh the times in the rankings website when a user logs in
# ----------------------------------------------------------------------------------------------------
def fetch_data_login():
        
        all_data = []

        for race_ID in range(1,19):
            course = "S"

            result_short = extract_data(race_ID, course, race_ID)

            if result_short != []:         
                all_data.append(result_short)


        for race_ID in range(19,36):
            course = "L"

            result_long = extract_data((race_ID - 18), course, race_ID)
            if result_long != []:
                all_data.append(result_long)


        result = all_data
        return result



# Function to format the times scraped from the rankings website into a consistent format for the database
# --------------------------------------------------------------------------------------------------------
def time_format(time_str):
    
    value = str(time_str).strip()
    if value == "":
        return None
    
    if ":" in value:
        return value
    
    else:
        value = "00:" + value
        return value
    


# Function to format date value to match format in database
# ---------------------------------------------------------
def date_format(date_str):

    value = str(date_str).strip()
    if value == "":
        return None
    
    if "-" in value:
        value = value.replace("-", "/")
        year, month, day = value.split("/")
        if len(year) == 4:
            year = year[2:]
        value = f"{day}/{month}/{year}"
        return value
    else:
        return value



