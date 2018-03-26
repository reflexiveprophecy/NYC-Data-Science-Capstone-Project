import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import pandas as pd


def parse(source, destination, date, optimize="price"):
	for j in range(5):
		try:
			url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source,destination,date)
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			response = requests.get(url, headers=headers, verify=False)
			parser = html.fromstring(response.text)
			json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
			raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
			flight_data = json.loads(raw_json["content"])
 
			flight_list = []

			for i in flight_data['legs'].keys():
				total_distance =  flight_data['legs'][i].get("formattedDistance",'')
				exact_price = flight_data['legs'][i].get('price',{}).get('totalPriceAsDecimal','')

				departure_location_airport = flight_data['legs'][i].get('departureLocation',{}).get('airportLongName','')
				departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
				departure_location_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')
				
				arrival_location_airport = flight_data['legs'][i].get('arrivalLocation',{}).get('airportLongName','')
				arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCode','')
				arrival_location_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
				airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')
				
				no_of_stops = flight_data['legs'][i].get("stops","")
				flight_duration = flight_data['legs'][i].get('duration',{})
				flight_hour = flight_duration.get('hours','')
				flight_minutes = flight_duration.get('minutes','')
				flight_days = flight_duration.get('numOfDays','')

				if no_of_stops==0:
					stop = "Nonstop"
				else:
					stop = str(no_of_stops)+' Stop'

				total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days,flight_hour,flight_minutes)
				departure = departure_location_airport+", "+departure_location_city
				arrival = arrival_location_airport+", "+arrival_location_city
				carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
				plane = carrier.get('plane','')
				plane_code = carrier.get('planeCode','')
				formatted_price = "{0:.2f}".format(exact_price)

				if not airline_name:
					airline_name = carrier.get('operatedBy','')
				
				timings = []
				for timeline in  flight_data['legs'][i].get('timeline',{}):
					if 'departureAirport' in timeline.keys():
						departure_airport = timeline['departureAirport'].get('longName','')
						departure_time = timeline['departureTime'].get('time','')
						arrival_airport = timeline.get('arrivalAirport',{}).get('longName','')
						arrival_time = timeline.get('arrivalTime',{}).get('time','')
						flight_timing = {
											'departure_airport':departure_airport,
											'departure_time':departure_time,
											'arrival_airport':arrival_airport,
											'arrival_time':arrival_time
						}
						timings.append(flight_timing)

				flight_details={'stops':stop,
					'ticket price':formatted_price,
					'departure':departure,
					'arrival':arrival,
					'flight duration':total_flight_duration,
					'airline':airline_name,
					'plane':plane,
					'timings':timings,
					'plane code':plane_code
				}
				flight_list.append(flight_details)

			# Convert to dataframe, sort and get top 10 options
			flight_df = pd.DataFrame(flight_list)
			flight_df.sort_values(by=[optimize], ascending = True, inplace = True)
			flight_df = flight_df.head(10)

			# Get best price
			flight_df_copy = flight_df.copy()
			flight_df_copy.sort_values(by="ticket price", ascending = True, inplace = True)
			best_price = float(flight_df_copy['ticket price'].head(1).values)
			return flight_df, best_price
		
		except ValueError:
			print ("Retrying...")
			
		return {"error":"failed to process the page",}, best_price

def check_csv_flights(source, destination, date):
	if source == "NYC":
		source_list = [' New York', " Newark"]
	else: 
		source_list = [' Los Angeles']

	if destination == "NYC":
		destination_list = [' New York', " Newark"]
	else: 
		destination_list = [' Los Angeles']

	flights = pd.read_csv("./Flight_Data/flights_250days_march17.csv")
	flights = flights[flights['departure'].isin(source_list)]
	flights = flights[flights['arrival'].isin(destination_list)]
	flights['date'] = flights['date'].astype(str)
	flights = flights[flights['date'] == date]

	flights.sort_values(by=['ticket price'], ascending = True, inplace = True)
	if flights.shape[0] > 0:
		best_price = flights['ticket price'].head(1).values[0]
	else:
		best_price = 999999999

	return best_price

######################### SUMMARY ###############################
# Get flight data from current and past flight, compare prices.
# Return whether price increased or not, and flight details for
# the two dates.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Inputs:
# 	- source (LAX as default)
#   - destination (NYC as default)
#   - date1 (start date, with format '06/15/2018')
#   - date2 (return date, with format '06/18/2018')
#   - optimize ("ticket price", duration, airline)
# Output:
#	- "price increased", flight_df1, flight_df2
#################################################################
def main_flights(source = "LAX", destination = "NYC", date1 = '06/14/2018', date2 = '06/17/2018'):

	# Get current flight data
	flight_df1, best_current_price_1 = parse(source,destination,date1,price)
	flight_df2, best_current_price_2 = parse(destination,source,date2,price)


	# Compare to 2 weeks ago flight prices
	best_old_price_1 = check_csv_flights(source,destination,date1)
	best_old_price_2 = check_csv_flights(destination,source,date2)


	# Price comparison
	current_price = best_current_price_1 + best_current_price_2
	old_price = best_old_price_1 + best_old_price_2

	difference = current_price - old_price

	if difference < -100000:
		return 'invalid price change', 0, flight_df1, flight_df2

	# Generating results
	if current_price > old_price:
		return 'best_price_increased', difference, flight_df1, flight_df2
	else:
		return 'best_price_decreased', difference, flight_df1, flight_df2

results = main_flights(source = "LAX", destination = "NYC", date1 = '06/14/2018', date2 = '06/17/2018')

print(results[0])
print(results[1])
print(results[2])
print(results[3])





