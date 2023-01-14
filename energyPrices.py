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

SETTLEMENT_PERIOD = "1"
SETTLEMENT_DATE = "2023-01-13"
API_KEY = "k9tx07nd96x51aa"
api_url = f"https://api.bmreports.com/BMRS/NETBSAD/v1?APIKey={API_KEY}&SettlementDate={SETTLEMENT_DATE}&SettlementPeriod={SETTLEMENT_PERIOD}&IsTwoDayWindow=false&ServiceType=CSV"

with requests.Session() as s: # Starts a request session
    download = s.get(api_url) # Gets the CSV from the url

    decoded_content = download.content.decode('utf-8') # Decodes the CSV into utf-8 string format

    csvReader = csv.reader(decoded_content.splitlines(), delimiter=',') # Reads the CSV with a reader object
    my_list = list(csvReader) # Object is converted to list
    
    with open(r"C:\Users\user\Documents\Homework\Young Engineers\API\data.csv", 'w') as file:
        writer = csv.writer(file) # Writer object created
        writer.writerows(my_list) # Writer object writes to file