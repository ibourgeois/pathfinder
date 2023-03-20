import requests, json

class DistanceAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_path(self, lat1, lon1, lat2, lon2):
        req_url_prep = 'https://api.openrouteservice.org/v2/directions/{type}?api_key={key}&start={start_lon},{start_lat}&end={end_lon},{end_lat}'
        req_url = req_url_prep.format(type = 'foot-walking', key = self.api_key, start_lat = lat1, start_lon = lon1, end_lat = lat2, end_lon = lon2)
        print(req_url)
        try:
            response = requests.get(req_url)
        except requests.exceptions.RequestException as e:
            print(response.text)
            raise SrystemExit(e)
        print(response.text)
        return json.loads(response.text)

    def test_get_path():
        with open('test_response.json') as test_response:
            parsed_json = json.load(test_response)
        return parsed_json
