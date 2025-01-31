import requests
import pprint
import time
import json
import datetime
import pytz
import math
import cv2
import numpy as np


def epoch_to_eastern(epoch_time):
    """Converts epoch time to Eastern Standard Time (EST)."""
    # print(f'Received >> {epoch_time} and type >> {type(epoch_time) }')
    

    # Create a datetime object from the epoch time
    dt = datetime.datetime.fromtimestamp(epoch_time, tz=pytz.utc)

    # Convert to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    dt_eastern = dt.astimezone(eastern)

    # Format the datetime object
    return dt_eastern.strftime('%Y-%m-%d %H:%M:%S %Z')

def relative_to_clock(remaining_time):

    seconds = remaining_time % 60
    minutes = math.floor(remaining_time / (60))
    hours = math.floor(remaining_time / (60*60))
    return str(f'{minutes} min {seconds} secs ')


def get_nearbyroutes(url, headers, params):
   
    
    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(f'Response : {response.status_code}\n')
            routes = response.json()
            return routes
        
        else:
            print(f'Invalid response with reponse code {response.status_code}')

    except requests.exceptions.RequestException as e:
        print('Error',e)
        return None



# Main Code



url = 'https://external.transitapp.com/v3/public/nearby_routes'

# url = 'https://external.transitapp.com/v3/public/nearby_routes'

headers = {
    'apikey' : '970d7e18d733c9a00b99386b22d0d31718809120780041913b8d651494bd6fcd'
}

params = {
    'lat' : 42.311366,
    'lon' : -71.092330,
    'max_distance' : 30

    # 'global_stop_id' : 'MBTA:88628',
    # 'remove_cancelled' : True,
    # 'should_update_realtime' : True
}


# for j in range(1):
#     busList = []
#     routes = get_nearbyroutes(url, headers, params)
    
#     if routes is not None:
#         for i in range(len(routes["route_departures"])):
#             print(f' Responses {i} >> \n {routes["route_departures"][i]["compact_display_short_name"]["elements"][1]} \n')
#             busList.append(routes["route_departures"][i]["compact_display_short_name"]["elements"][1])
            
#     else:
#         print(f'Max limit reached')
#     print(f'List of all available lines : {busList}')
#     time.sleep(2)
   
while True:

    routes = get_nearbyroutes(url , headers, params)

    print(f'Bus Number >> {routes["routes"][1]["compact_display_short_name"]["elements"][1]}')
    # print(f'{routes["routes"][1]["itineraries"][0]["schedule_items"][0]["departure_time"]}')
    direction_headsign = routes["routes"][1]["itineraries"][1]["direction_headsign"]
    print(f'Direction Headsign >> {direction_headsign}')

    current_time = int(time.time())

    app_window = np.zeros((480,1000,3), dtype=np.uint8)




    for i in range(len(routes["routes"][1]["itineraries"][1]["schedule_items"])):
        epoch_time = int(routes["routes"][1]["itineraries"][1]["schedule_items"][i]["departure_time"])
        is_real_time = routes["routes"][1]["itineraries"][1]["schedule_items"][i]["is_real_time"]
        remaining_time = int(epoch_time-current_time)
        scheduled_time = epoch_to_eastern(epoch_time)

        print(f'Scheduled time {i}>> {scheduled_time} :: is_real_time >> {is_real_time} :: Current time >> {relative_to_clock(remaining_time)}')
        
        cv2.putText(app_window, str(direction_headsign), (850, 25), 2,1, (255,255,255), 1,1)
        cv2.putText(app_window, str(remaining_time), (850, 300+i*40), 2,1, (255,255,255), 1,1)



    cv2.imshow("App Window", app_window)


    cv2.waitKey(2000)




# with open("data.json","w") as file:
#     json.dump(routes, file, indent= 4, sort_keys= True)



