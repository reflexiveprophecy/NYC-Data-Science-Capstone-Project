import pandas as pd 


####### Summary: ############
# Input:
#    - num_guests 1-15
#    - num_rooms 0-10
#    - room_type "Entire home/apt", "Private room", "Shared room"
#    - max_price "100"
#    - checkin_date '06/14/2018'
#    - checkout_date '06/14/2018'
#    - min_rating 0-100
#    - num_beds 0-5
#    - best_price (boolean)
#			- if true, put 5 "Good Deals" on top, followed by the rest of dataframe sorted by price
# 			- if false, put 3 "Good Deals" on top from top 1000 results, followed by rest of dataframe 
#    - df, wenchangs already ordered dataframe on the string search
# Output:
#    - room_df, filtered
def filter_dataframe(num_guests = 1,
					 num_rooms = 1,  
					 room_type = "Private room",
					 max_price = 150, 
					 checkin_date = '06/14/2018',
					 checkout_date = '06/17/2018', 
					 min_rating = 0, 
					 num_beds = 1, 
					 best_price = False,
					 nlp_df = None):





	# NOTE TO ROGER, YOU WILL NEED TO REPLACE room_df WITH nlp_df (FROM WENCHANG)
	# YOU WILL ALSO NEED TO REPLACE THE FILE PATH TO avail_df, and verify that "id" is "id" in the csv
	####################################################################
	# Get dates csv
	avail_df = pd.read_csv("./Room_Data/nypriceavail.csv")
	# Get room csv
	room_df = pd.read_csv("./Room_Data/finalmergedlisting.csv")
	####################################################################






	# Join csvs together
	room_df = pd.merge(avail_df, room_df, on='id')

	room_df = room_df[room_df['accommodates']          == num_guests]
	room_df = room_df[room_df['bedrooms']              == num_rooms]
	room_df = room_df[room_df['room_type']             == room_type]
	room_df = room_df[room_df['price']                 <  max_price]
	room_df = room_df[room_df['beds']                  == num_beds]

	if min_rating != 0:
		room_df = room_df[room_df['review_scores_rating']  >  min_rating]

	# Convert dates here from '06/14/2018' to '2018/06/14' for room lookup
	month_in = checkin_date[0:2]
	day_in = checkin_date[3:5]
	year_in = checkin_date[6:10]

	month_out = checkout_date[0:2]
	day_out = checkout_date[3:5]
	year_out = checkout_date[6:10]

	checkin_date_room = year_in + "-" + month_in + "-" + day_in
	checkout_date_room = year_out + "-" + month_out + "-" + day_out

	# Filter on check in and check out days
	start_col = room_df.columns.get_loc(checkin_date_room)
	final_col = room_df.columns.get_loc(checkout_date_room)

	# Filter on minimum nights
	room_df = room_df[room_df['minimum_nights'] <  final_col - start_col]

	# Check every column including the ends and see if they are labeled "" or not
	for col_num in range(start_col,final_col+1):
		room_df = room_df[room_df[room_df.columns[col_num]].isnull() == False]

	# Ordering here
	if best_price:
		room_df.sort_values(by=['price'], ascending = True, inplace = True)

	partial_df = room_df.head(500)
	mask = (partial_df['price_good'] == "Good Deal") & (partial_df['price'] > 10)
	partial_df = partial_df[mask]
	partial_df.sort_values(by=['price'], ascending = True, inplace = True)
	partial_df = partial_df.head(3)
	duplicate_ids = partial_df[['id']]
	room_df = room_df[-room_df['id'].isin(duplicate_ids)]
	frames = [partial_df, room_df]
	room_df = pd.concat(frames)

	return room_df



# Test region:

# results = filter_dataframe(num_guests = 1,
# 					 num_rooms = 1,  
# 					 room_type = "Private room",
# 					 max_price = 450, 
# 					 checkin_date = '10/14/2018',
# 					 checkout_date = '10/17/2018', 
# 					 min_rating = 0, 
# 					 num_beds = 1, 
# 					 best_price = True,
# 					 nlp_df = None)
# print(results.head(5))
# print(results['price'][0:5])

