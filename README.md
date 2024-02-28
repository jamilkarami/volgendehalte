This Flask application uses the Here Maps API to find the incoming buses at bus stops in the Netherlands. (Only tested in Eindhoven with Bravo/Hermes, but theoretically should work for other cities/bus companies if they publish the same information)

It's a really simple "app" that really only does one thing and that I wrote to use in other projects. (I currently have a Pi Zero calling this then showing me bus info on a matrix display)

You call an endpoint and it returns data in this format:

```json
// /bus?count=3
[
    {"number": "123", "eta": 5, "time": "13 Jan 2024 21:30:00"}, 
    {"number": "234", "eta": 8, "time": "13 Jan 2024 21:33:00"}, 
    {"number": "345", "eta": 12, "time": "13 Jan 2024 21:37:00"}
]
```

### How to use

Fill the `settings.py` file with your settings, spin up a Docker container from the dockerfile and then call `http://YOUR_PC_IP_ADDRESS:5000/bus?count=COUNT_HERE` (count is optional. defaults to 3) to get the incoming buses that are ETA+ minutes out.

You can get the station ID for your station of choice by calling `https://transit.hereapi.com/v8/stations?in=[LATITUDE],[LONGITUDE]` (find those on any maps app). You need a [HERE Maps API key](https://www.here.com/docs/), which you'll also have to put in the [settings.py](settings.py) file