import datetime as dt
import pytz

from flask import Flask, request

import requests

import settings

app = Flask(__name__)

tz = pytz.timezone(settings.TIMEZONE)

here_api_url = "https://transit.hereapi.com/v8/departures?ids={}&apiKey={}"


def get_next_buses(count):
    data = requests.get(
        here_api_url.format(settings.BUS_STOP_ID, settings.HERE_API_KEY)
    ).json()

    buses = data["boards"][0]["departures"]

    if not buses:
        print("No buses")

    valid_buses = [v_bus for bus in buses if (v_bus := val(bus)) is not None]
    valid_buses.sort(key=lambda bus: bus["eta"])

    if not valid_buses:
        return {"Error": "No buses found"}

    return valid_buses[:count]


@app.route("/bus")
def bus():
    num = request.args.get("count", default=3, type=int)
    buses = get_next_buses(num)
    return buses


def val(bus) -> bool:
    bus_time = bus["time"]
    bus_number = bus["transport"]["name"]
    delay = bus.get("delay", 0)
    current_time = dt.datetime.now(tz)

    time_del = dt.datetime.fromisoformat(bus_time).replace(tzinfo=None) + dt.timedelta(seconds=delay)
    minutes_until = (time_del.hour - current_time.hour) * 60 + (time_del.minute - current_time.minute)

    if minutes_until >= settings.ETA:
        return {
            "number": bus_number,
            "eta": minutes_until,
            "time": time_del
        }
    return None


app.run(host="0.0.0.0")  # pass the host parameter to expose to local network
