import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import pandas as pd
import datetime as dt
import itertools
from time import sleep
import time
import random
import urllib3
from lxml.html import fromstring
import re
from queue import *
import boto3
from multiprocessing import Pool
import multiprocessing as mp
import signal
from timeout import timeout

import sys
print(sys.path)

######### Quick Guide to using Crontabs ##########

# Every 5 mins
# $ */5 * * * * /anaconda/bin/python /Users/adodd202/Documents/Bootcamp_Spring2018/NYC-Data-Science-Capstone-Project/Andrew/expediaScrapeAll.py

# To delete mail:
# $ cat /dev/null >/var/mail/adodd202

# To see mail:
# $ mail

#################################################

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 '},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.15; Mac_PowerPC)'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.15'},
    {'User-Agent': 'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/85.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3'}]


######################### SUMMARY ###############################
# Performs query on Expedia for one day, one destination and one 
# source city. 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Inputs:
# 	- Query: this is a list of lists. 1st element is date. 2nd 
#     element is a list with source, destination.
# Output:
#	- sortedList: This is a list of dictionaries with flight 
#     details of each flight in this query.
#################################################################
def parse(query):
	source = query[1][0]
	destination = query[1][1]
	date = query[0]
	# proxies is global variable

	print("starting parser"+"="*50)
	sleep(random.uniform(3,5))

	scrape_date = dt.datetime.today()
	scrape_date = scrape_date.strftime('%m/%d/%Y')

	# Iterating 5 times, sometimes a proxy fails, so we retry this a few times. If proxy fails 5 times, we return "Error."
	for i in range(5):
		print("new forloop iteration")
		proxy = random.sample(proxies, 1)
		prev_proxy = proxy

		# Some proxies don't work, we will try a few of them.
		try:
			# # Get a random proxy, make sure it was not the most recent proxy
			while proxy == prev_proxy:
				proxy = random.sample(proxies, 1)
				proxy = proxy[0]
				print("Getting different proxy")
			prev_proxy = proxy

			# Get random header
			headers = random.sample(headers_list, 1)
			headers = headers[0]

			print(proxy)
			print("got headers, getting url and starting response")
			url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source,destination,date)

			response = requests.get(url, headers=headers, verify=False, proxies={"http": proxy, "https": proxy}, timeout = 5)

			# If the response comes back good, we create dictionary.
			if response.status_code == 200:
				parser = html.fromstring(response.text)
				json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
				raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
				flight_data = json.loads(raw_json["content"])
	 
				lists=[]
				print("going through flight_data")
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

					if flight_data['legs'][i].get('timeline',[])[0] is not None:
						carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
					else:
						carrier = ''

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

					flight_info={'stops':stop,
						'ticket price':formatted_price,
						'departure':departure,
						'arrival':arrival,
						'flight duration':total_flight_duration,
						'airline':airline_name,
						'plane':plane,
						'timings':timings,
						'plane code':plane_code,
						'date':date,
						'scrape_date':scrape_date
					}

					# Add each flight info to our list of flight infos.
					lists.append(flight_info)

				# Sort by price and return the list.
				sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
				print("Adding to list of Expedia flights")
				return sortedlist

			# If the response is bad, we show error.
			else: 
				print('Error Code {}'.format(response.status_code))

		# In some cases, our response(url) will give an error (503, 404, 403, etc.). This could be due to proxy server 
		# error from overusing proxies, Expedia not responding to a certain proxy, or just no response from the server.
		# Here we catch all exceptions, print them, and then go to next loop iteration.
		except Exception as e:
			print ("Error is {}".format(e))
			print ("Retrying...")
			
	# This was indented further in before, but I think we want to return here (not inside forloop).
	# This will allow loop to run.
	return {"error":"failed to process the page",}

######################### SUMMARY ###############################
# This gets a list of good fast proxies. (tested, most 2 second
# response)
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Inputs: None
# Output:
#	- List of proxies
#################################################################
def get_proxies(num_proxies = 10):
	print("INTIALIZING {} PROXIES".format(num_proxies))

	# Go to the proxy list url, and get their website text
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	parser = fromstring(response.text)

	proxies = set()
	# For each potential proxy, add it if it works.
	for i in parser.xpath('//tbody/tr'):
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			#Grabbing IP and corresponding PORT
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])

			try:
				sleep(.5)
				# Check the proxy
				urls = ["http://www.neopets.com/", "https://www.theatlantic.com/", "https://www.reddit.com/r/funny/", "http://www.pythonforbeginners.com/"]
				url = random.sample(urls, 1)[0]
				print(url)
				print(proxy)

				with timeout(seconds=2):
					response = requests.get(url,proxies={"http": proxy, "https": proxy})

				# If it works, add the proxy
				proxies.add(proxy)

				print("="*50)
				print("We have added {} proxies of a total of {} proxies".format(len(proxies),num_proxies))
				print("{}% Complete with initializing proxies".format(round(len(proxies)/num_proxies*100,2)))

				if len(proxies) == num_proxies:
					return proxies
			except:
				print("Failed Connection")
				continue
	return proxies


# Generating global proxy list
num_proxies = 2
proxies = get_proxies(num_proxies)

def main():
	with timeout(seconds=3):
		sleep(2)

	# Creating airport pairs to iterate
	airports = ["NYC", "LAX"]#, "CHI", "BOS", "SFO"]
	airport_pairs = list(itertools.permutations(airports, 2))

	# Creating dates to iterate
	num_days = 1
	base = dt.datetime.today() + dt.timedelta(days=1)
	dates = [base + dt.timedelta(days=x) for x in range(0, num_days)]
	dates = list(map(lambda x: x.strftime('%m/%d/%Y'), dates))
	total_length = len(airport_pairs) * num_days

	# Generate list of queries for pool
	queries = [[date,pair] for date in dates for pair in airport_pairs]

	# Going through all results
	print ("Fetching flight details")

	# Starting multiprocessing
	pool = mp.Pool(2)
	list_flights = pool.map(parse, queries)
	pool.terminate()
	pool.join()

	print("done with results")

	with open('/Users/adodd202/Documents/Bootcamp_Spring2018/NYC-Data-Science-Capstone-Project/flight-results-all.json','w') as fp:
		json.dump(list_flights,fp,indent = 4)

	# This is for further development.
	# save_to_s3(list_flights) # ADD ME LATER ON EC2

main()




# Function still in development

# def save_to_s3(json_data):
# 	timestr = time.strftime("%Y%m%d-%H%M%S")
# 	bucket_name = 'ruminator'
# 	file_key = "flights_" + timestr + ".json"

# 	s3_connection = boto.connect_s3()
# 	bucket = s3_connection.get_bucket('ruminator')
# 	key = boto.s3.key.Key(bucket, file_key)
# 	with open(file_key) as f:
# 		key.send_file(f)





