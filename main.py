import requests
from datetime import datetime
import smtplib
import config

MY_LAT = -29.6604  # Your latitude
MY_LONG = -51.0562  # Your longitude


def is_iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    # data = response.json()
    iss_lat = float(response.json()["iss_position"]["latitude"])
    iss_long = float(response.json()["iss_position"]["longitude"])

    print(f"MY_LAT {MY_LAT + 3} ~ {MY_LAT - 3}")
    print(f"MY_LONG {MY_LONG + 3} ~ {MY_LONG - 3}")
    print(f"iss DATA {iss_lat} {iss_long}")
    # iss_lat = -30
    # iss_long = -48
    # Your position is within +5 or -5 degrees of the iss position.
    if (iss_lat <= MY_LAT + 3 or iss_lat <= MY_LAT - 3) and (iss_long <= MY_LONG + 3 or iss_long <= MY_LONG - 3):
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
    # current_hour = 20

    if sunrise <= current_hour <= sunset:
        return False  # It's daytime
    return True  # It's nighttime


def send_email():
    msg = f"ISS is near from you"
    connection = smtplib.SMTP("smtp.gmail.com")
    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}'
    connection.starttls()
    connection.login(user=config.email_sender, password=config.password_sender)
    connection.sendmail(from_addr=config.email_sender, to_addrs=config.email_receiver, msg=fmt.format
                        (config.email_receiver, config.email_sender, config.subject, msg).encode('utf-8'))
    connection.close()


print(is_iss_near())
print(is_dark())

# If the iss is close to my current position
# ,and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.

if is_iss_near() and is_dark():
    send_email()
