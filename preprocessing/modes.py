from enum import Enum
import json, os
import requests
from coordinates import Coordinates
from dotenv import load_dotenv

load_dotenv()


class Mode(Enum):
    AIRPLANE = 0
    TRAIN = 1
    CAR = 2


class Route:
    def __init__(self, mode, distance, duration) -> None:
        self.mode = mode
        self.distance = distance
        self.duration = duration


@staticmethod
def _get_routes(from_: Coordinates, to: Coordinates) -> list[Mode]:
    def get_routes(mode, from_: Coordinates, to: Coordinates):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"

        payload = json.dumps(
            {
                "origin": {
                    "location": {
                        "latLng": {
                            "latitude": from_.lat,
                            "longitude": from_.lon,
                        }
                    }
                },
                "destination": {
                    "location": {
                        "latLng": {
                            "latitude": to.lat,
                            "longitude": to.lon,
                        }
                    }
                },
                "travelMode": mode,
                "computeAlternativeRoutes": True,
            }
        )

        api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters",
        }

        response = requests.post(url, headers=headers, data=payload)
        if not response.json():
            return []
        else:
            match mode:
                case "DRIVE":
                    return Mode.CAR
                case "TRANSIT":
                    return Mode.TRAIN

    drive = get_routes("DRIVE", from_, to)
    tr = get_routes("TRANSIT", from_, to)
    return drive, tr


def get_available_modes(from_, to) -> list[Mode]:
    result = [Mode.AIRPLANE]
    drive, tr = _get_routes(from_, to)
    result.append(drive) if drive != [] else result
    result.append(tr) if tr != [] else result
    return result
