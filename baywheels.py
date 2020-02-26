import requests, os
import fast_requests as fs
from geopy import distance

LAT = 37.771692797576797
LON = -122.44456551980454

print(os.environ)

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
API_KEY = os.environ.get('API_KEY')
MEMBER_ID = os.environ.get('MEMBER_ID')


class BayWheelsAPI:

	def __init__(self):
		self.urls = {}
		self.urls['mapdata'] = 'https://layer.bicyclesharing.net/map/v1/fgb/map-inventory'
		self.urls['rent'] = 'https://layer.bicyclesharing.net/mobile/v2/fgb/rent'
		self.auth = AUTH_TOKEN
		self.api_key = API_KEY
		self.memberId = MEMBER_ID

		self.headers = {'api-key':self.api_key, 'authorization':self.auth}
		

	def get_mapdata(self):
		return requests.get(self.urls['mapdata']).json()


	def post_rent(self, bike_id, lat=LAT, lon=LON): # TODO: remove defaults
		data = {}
		data['userLocation'] = {'lat':lat,'long':lon} # TODO: maybe toFloat?
		data['qrCode'] = {'memberId':self.memberId, 'qrCode':str(bike_id)}
		return requests.post(self.urls['rent'], headers=self.headers, json=data)


	def find_station_by_name(self, name):
		stations = self.get_mapdata()['features']
		return next((s for s in stations if s['properties']['station']['name'] == name), None)


	def find_nearest_station(self, lat, lon):
		stations = self.get_mapdata()['features']

		def dist(station):
			station_coords = tuple(station['geometry']['coordinates'])[::-1]
			return distance.distance(station_coords, (lat,lon))

		return min(stations, key=dist)


if __name__ == '__main__':
	api = BayWheelsAPI()


