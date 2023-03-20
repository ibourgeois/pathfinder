import requests, json, random

class DistanceAPIClient:
    def __init__(self, api_key, profile):
        self.api_key = api_key
        self.profile = profile

    def get_path(self, lat1, lon1, lat2, lon2):
        req_url_prep = 'https://api.openrouteservice.org/v2/directions/{profile}?api_key={key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
        req_url = req_url_prep.format(profile = self.profile, key = self.api_key, start_lat = lat1, start_lon = lon1, end_lat = lat2, end_lon = lon2)
        try:
            response = requests.get(req_url)
        except requests.exceptions.RequestException as e:
            print(response.text)
            raise SrystemExit(e)
        return json.loads(response.text)

    def random_path(self):
        return random.randrange(1, 100, 1)

    def generate_result_path(self, points):
        headers = {
        'Authorization': self.api_key
        }
        data = {"coordinates": points}
        req_url_prep = 'https://api.openrouteservice.org/v2/directions/{profile}/gpx'
        req_url = req_url_prep.format(profile = self.profile)
        response = requests.post(req_url, headers=headers, json=data)
        return response.text
