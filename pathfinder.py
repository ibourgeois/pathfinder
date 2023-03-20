import itertools

class ShortestPath:
    def __init__(self, locations, distance_api):
        self.locations = locations
        self.distance_api = distance_api

    def get_shortest_path(self):
        shortest_distance = None
        shortest_path = None
        for path in itertools.permutations(self.locations):
            distance = 0
            for i in range(len(path)-1):
                lat1, lon1 = path[i]
                lat2, lon2 = path[i+1]
                distance += self.distance_api.get_distance(lat1, lon1, lat2, lon2)
            if shortest_distance is None or distance < shortest_distance:
                shortest_distance = distance
                shortest_path = path
        return shortest_path
