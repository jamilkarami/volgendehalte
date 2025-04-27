import datetime as dt
import pytz
import dotenv
import os
from flask import Flask, request

import requests

app = Flask(__name__)

dotenv.load_dotenv()

tz = pytz.timezone(os.getenv("TIMEZONE"))

here_api_url = f"https://transit.hereapi.com/v8/departures?ids={os.getenv('BUS_STOP_ID')}&apiKey={os.getenv('HERE_API_KEY')}"


def get_next_buses(count):
    data = requests.get(here_api_url).json()

    departures = data["boards"][0]["departures"]

    valid_buses = [v_bus for departure in departures if (v_bus := val(departure)) is not None]
    valid_buses.sort(key=lambda departure: departure["eta"])

    if not valid_buses:
        return {"Error": "No buses found"}

    return valid_buses[:count]


@app.route("/bus")
def bus():
    num = request.args.get("count", default=3, type=int)
    buses = get_next_buses(num)
    return buses


def val(bus_info):
    bus_time = bus_info["time"]
    bus_number = bus_info["transport"]["name"]
    delay = bus_info.get("delay", 0)
    current_time = dt.datetime.now(tz)

    time_del = dt.datetime.fromisoformat(bus_time).replace(tzinfo=None) + dt.timedelta(seconds=delay)
    minutes_until = (time_del.hour - current_time.hour) * 60 + (time_del.minute - current_time.minute)

    if minutes_until >= int(os.getenv("ETA")):
        return {
            "number": bus_number,
            "eta": minutes_until,
            "time": time_del
        }
    return None


app.run(host="0.0.0.0")  # pass the host parameter to expose to local network
