from openrouteservice import DistanceAPIClient
from pathfinder import ShortestPath
from dotenv import load_dotenv
import os

load_dotenv()

locations = [
    (49.206677, 16.605728),
    (49.207589, 16.608298),
    (49.205349, 16.608185),
    (49.206054, 16.609060),
    (49.204382, 16.606715),
]

distance_api = DistanceAPIClient(os.getenv("API_KEY"))
shortest_path = ShortestPath(locations, distance_api)
# path = shortest_path.get_shortest_path()
path = distance_api.get_path(49.2016811, 16.6106769, 49.2049758, 16.6133592)
p = path['features'][0]['properties']['segments'][0]['distance']
print(p)
# print(path)