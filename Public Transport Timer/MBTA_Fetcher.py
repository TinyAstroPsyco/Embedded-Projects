import requests
import json
from datetime import datetime, timedelta 
import pytz
import numpy as np
import cv2



def fetch():

    # Base URL and Endpoint for the MBTA Website
    BASE_URL = "https://api-v3.mbta.com"
    ENDPOINT = "/predictions"  # You can change this to other endpoints like /routes, /stops, etc.

    API_KEY = "a7ce3bd86d3d4fb4ac2cfa39138c3396"

    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "accept": "application/json"
    }


    PARAMS = {
        "filter[stop]": "1742",  # Replace with your stop ID
        # "filter[direction_id]": "0",    # Optional: Direction (e.g., 0 or 1)
        # "include": "stop"              # Include stop details in the response
        "filter[latitude]" : "42.312322052258686",
        "filter[longitude]" : "-71.0934255584537",
        "filter[radius]" : ".01",
        "filter[route]": '22',
        "filter[direction_id]" : "1"

    }


    response = requests.get(f"{BASE_URL}{ENDPOINT}", headers=HEADERS, params= PARAMS)

    timing = []
    if response.status_code == 200:
        data = response.json()
        print("✅ API Request Successful!")
        # print(data)  # Print the API response data
    else:
        print(f"❌ API Request Failed with status code: {response.status_code}")
        # print(response.text)  # Print error details

    with open("prediction_data_without key.json","w") as file:
        json.dump(data, file, indent= 4, sort_keys= True)
    
    
    for i in range(len(data["data"])):
        # print(f'Data >> {data["data"][i]["attributes"]["arrival_time"]}')
        time_stamp = str(data["data"][i]["attributes"]["arrival_time"])
        time_stamp = datetime.fromisoformat(time_stamp)
        # print(f'✅ Parsed Timestamp: {time_stamp}')
        current_time = datetime.now(pytz.timezone("US/Eastern"))  # Adjust this timezone if necessary
        # print(f'🕒 Current time: {current_time}')
        
        # Calculate the remaining time
        time_difference = time_stamp - current_time
        # print(f'⏳ Time Remaining: {time_difference}')

        # Breakdown into hours, minutes, and seconds
        total_seconds = int(time_difference.total_seconds())
        print(f'Total Seconds >> {total_seconds}')
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # print(f'🕑 Remaining Time: {hours}h {minutes}m {seconds}s')
        time_data = {
                "h" : hours,
                "m" : minutes,
                "s" : seconds,
                "total_seconds" : total_seconds
        }

        timing.append(time_data)
     

        # cv2.putText(app_window, str(direction_headsign), (850, 25), 2,1, (255,255,255), 1,1)
        # cv2.putText(app_window, (str(hours) +"h " + str(minutes) + "m " + str(seconds) + "s"), (650, 300+i*40), 2,1, (255,255,255), 1,1)
    
    
    
    
    # print(f'Dictionary >> {time_data}')
    
    
    return timing





app_window = np.zeros((480,1000,3), dtype=np.uint8)


while False:
    data = fetch()
    # print(f'Data >> {data[]["attributes"]["arrival_time"][0]}')
    for i in range(len(data["data"])):
        # print(f'Data >> {data["data"][i]["attributes"]["arrival_time"]}')
        time_stamp = str(data["data"][i]["attributes"]["arrival_time"])
        time_stamp = datetime.fromisoformat(time_stamp)
        # print(f'✅ Parsed Timestamp: {time_stamp}')
        current_time = datetime.now(pytz.timezone("US/Eastern"))  # Adjust this timezone if necessary
        # print(f'🕒 Current time: {current_time}')
        
        # Calculate the remaining time
        time_difference = time_stamp - current_time
        # print(f'⏳ Time Remaining: {time_difference}')

        # Breakdown into hours, minutes, and seconds
        total_seconds = int(time_difference.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f'🕑 Remaining Time: {hours}h {minutes}m {seconds}s')

        # cv2.putText(app_window, str(direction_headsign), (850, 25), 2,1, (255,255,255), 1,1)
        cv2.putText(app_window, (str(hours) +"h " + str(minutes) + "m " + str(seconds) + "s"), (650, 300+i*40), 2,1, (255,255,255), 1,1)


    cv2.imshow("GUI", app_window)
    app_window[:] = 0

    cv2.waitKey(10000)