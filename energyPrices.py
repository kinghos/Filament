import datetime
import requests
import csv
import pandas as pd

def settlementPeriod(time):
    # now = datetime.datetime.now()
    hours = time.strftime("%H")
    mins = time.strftime("%M")
    hours, mins = int(hours), int(mins)
    mins += hours * 60
    return mins // 30 + 1 # Settlement periods calculated

START_DATE = "13-01-2023"
END_DATE = "14-01-2023"
DNO = 12
VOLTAGE = "LV"
api_url = f"https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices?{DNO}&{VOLTAGE}&P{START_DATE}&{END_DATE}"

with requests.Session() as s: # Starts a request session
    download = s.get(api_url) # Gets the CSV from the url

    decoded_content = download.content.decode('utf-8') # Decodes the CSV into utf-8 string format

    csvReader = csv.reader(decoded_content.splitlines(), delimiter=',') # Reads the CSV with a reader object
    my_list = list(csvReader) # Object is converted to list
    
    with open(r"C:\Users\user\Documents\Homework\Young Engineers\API\data.csv", 'w') as file:
        writer = csv.writer(file) # Writer object created
        writer.writerows(my_list) # Writer object writes to file
    
    