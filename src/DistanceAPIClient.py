import requests, json, random, time

class DistanceAPIClient():
    def __init__(self, api_key, profile):
        self.api_key = api_key
        self.profile = profile

    def get_distance(self, lat1, lon1, lat2, lon2):
        """
        get_distance ... Function contacts the openrouteservice API and returns
        the distance between two points.
        """
        req_url_prep = 'https://api.openrouteservice.org/v2/directions/{profile}?api_key={key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
        req_url = req_url_prep.format(
            profile = self.profile,
            key = self.api_key,
            start_lat = lat1,
            start_lon = lon1,
            end_lat = lat2,
            end_lon = lon2)
        response = self.make_request(req_url)
        path = json.loads(response.text)
        if 'features' in path:
            return path['features'][0]['properties']['segments'][0]['distance']
        else:
            time.sleep(60)
            response = self.make_request(req_url)
            path = json.loads(response.text)
            if 'features' in path:
                return path['features'][0]['properties']['segments'][0]['distance']
            else:
                print(response.text)
                raise SystemExit(e)

    def make_request(self, req_url):
        try:
            response = requests.get(req_url)
        except requests.exceptions.RequestException as e:
            print(response.text)
            raise SystemExit(e)
        return response

    def get_random_distance(self):
        """
        get_random_distance ... Function returns random distance between two points.
        Mainly for testing purposes.
        """
        return random.randrange(1, 100, 1)

    def generate_result_path(self, points):
        """
        generate_result_path ... Function contacts the openrouteservice API and
        returns the route through given list of points.
        """
        headers = {
        'Authorization': self.api_key
        }
        data = {
            "coordinates": points,
            "instructions": "false"
        }
        req_url_prep = 'https://api.openrouteservice.org/v2/directions/{profile}/gpx'
        req_url = req_url_prep.format(profile = self.profile)
        response = requests.post(req_url, headers=headers, json=data)
        return response.text
