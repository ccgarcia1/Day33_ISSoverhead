import requests
from datetime import datetime

MY_LAT = -29.6604 # Your latitude
MY_LONG = -51.0562 # Your longitude

def is_ISS_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    #data = response.json()
    ISS_lat = float(response.json()["iss_position"]["latitude"])
    ISS_long = float(response.json()["iss_position"]["longitude"])

    print(f"MY_LAT {MY_LAT + 3} ~ {MY_LAT - 3}" )
    print(f"MY_LONG {MY_LONG + 3} ~ {MY_LONG - 3}" )
    print(f"ISS DATA {ISS_lat} {ISS_long}")
    #ISS_lat = -30
    #ISS_long = -48
    #Your position is within +5 or -5 degrees of the ISS position.
    if (ISS_lat <= MY_LAT + 3 or ISS_lat <= MY_LAT - 3 ) and (ISS_long <= MY_LONG + 3 or ISS_long <= MY_LONG - 3 ):
        return True
    return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": "America/Sao_Paulo"
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    print(f"{sunrise} {sunset}")
    current_hour = datetime.now().hour
    print(current_hour)
    #current_hour = 20

    if sunrise <= current_hour <= sunset:
        return False # It's daytime
    return True # It's nighttime


print(is_ISS_near())
print(is_dark())

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

if is_ISS_near() and is_dark():
    pass # build the logic to send an email



