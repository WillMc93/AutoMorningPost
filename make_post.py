import json
from datetime import datetime

import pandas as pd

from IssuetrakAPI import IssuetrakAPI


CATEGORIES_PATH = './categories.idk'
SEVENTEEN_SCHEDULE = './017_schedule.csv'


# Gather all tickets for the post.
# TODO: Try and make the request query readable
def get_tickets() -> pd.DataFrame:
	# Ugh, what a pain in the . . . 
	# They made this as obtuse as possible. Like is there a good reason to do it this way?
	# Why all of this spaghetti? This isn't even maximum possible spaghetti when searching.
	request = {
		'QuerySetDefinitions': [
			{ 
				'QuerySetIndex': 0, 'QuerySetOperator': 'AND', 'QuerySetExpressions': [
					{
						'QueryExpressionOperator': 'AND',
						'QueryExpressionOperation': 'Equal',
						'FieldName': 'Status',
						'FieldFilterValue1': 'Open',
						'FieldFilterValue2': ''
					}
				]
			}
		],
		'PageIndex': 0,
		'PageSize': 100,
		'CanIncludeNotes': False,
	}

	# Initialize API connection
	api = IssuetrakAPI.IssuetrakAPI()

	# Loop through and gather all open tickets
	tickets = []
	gathered_all = False
	total = 0
	while not gathered_all:
		# POST search request
		response = api.performPost('/issues/search/', '', json.dumps(request))

		# Convert json to python dictionary
		data = response.read()
		data = json.loads(data)

		# Get ticket data
		tickets += data['Collection']

		# Check loop status
		page_count = data['CountForPage'] # number of tickets on this 'page'
		expected_total = data['TotalCount'] # maximum number of open tickets
		total += page_count
		if total <  expected_total:
			request['PageIndex'] += 1
		else:
			gathered_all = True

	tickets = pd.DataFrame(tickets)
	print(tickets)

	return tickets
	

# Get the categories w/ custom strings.
def get_categories(path:str=CATEGORIES_PATH) -> dict:

	pass


# Get the 017 schedule from file
def get_schedule(path:str=SEVENTEEN_SCHEDULE) -> dict:

	pass

# Trim to neccessary columns and then picks out tickets for morning post
def process_tickets(tickets:pd.DataFrame) -> pd.DataFrame:

	#print(tickets.columns)

	# Filter down to needed columns
	columns = ['IssueNumber', 'SubmittedDate', 'Subject', 'IssueTypeID',
			   'AssignedTo', 'SubStatusID', 'RequiredByDate']
	tickets = tickets[tickets.columns.intersection(columns)]

	# Filter down to relevant rows

	return tickets


# Sort the tickets into the proper categories.
def sort_tickets(tickets:dict, categories:dict) -> dict:

	pass


# Create the necessary html string for posting in Teams
def render_post() -> str:

	pass


def main():
	# Get necessary info
	tickies = get_tickets()
	categories = get_categories()
	schedule = get_schedule()

	# Process and sort tickets
	tickies = process_tickets(tickies)
	print(tickies.head())
	tickie_dict = sort_tickets(tickies, categories)

	# Generate the post
	post = render_post()

	# Print the post for copying
	print(post)


if __name__ == '__main__':
	main()
