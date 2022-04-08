import json
from datetime import datetime

import jinja2 
import pandas as pd


from IssuetrakAPI import IssuetrakAPI

# Initialize Globals
POST_TEMPLATE = './post_template.j2'
SEVENTEEN_SCHEDULE = './017_schedule.csv'

# FUCK YOU APPLE; I DIDN'T NEED THIS SHIT IN LINUX TO SEE WHAT I WAS DOING
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


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

	# Convert tickets to DataFrame and return
	tickets = pd.DataFrame(tickets)
	return tickets
	

# Get the categories w/ custom strings.
def get_categories(path:str=CATEGORIES_PATH) -> dict:

	pass


# Get the 017 schedule from file
def get_schedule(path:str=SEVENTEEN_SCHEDULE) -> dict:

	pass


# Get a dictionary of substatus ids
def get_substatuses() -> dict:
	# Initialize API connection
	api = IssuetrakAPI.IssuetrakAPI()

	# GET data to dictionary
	response = api.performGet('/substatuses')
	data = response.read()
	data = json.loads(data)

	# Get IDs and their labels into a dictionary
	total = data['TotalCount']
	substatuses = data['Collection']
	substatuses = {id_['SubStatusID']: id_['SubStatusName'] for id_ in substatuses}
	assert(total == len(substatuses))

	return substatuses


# Get a dictionary of IssueTypeIDs
def get_issuetypes() -> dict:
	# Initialize API connection
	api = IssuetrakAPI.IssuetrakAPI()

	# GET data to dictionary
	response = api.performGet('/issuetypes')
	data = response.read()
	data = json.loads(data)

	# Get IDs and their labels into a dictionary
	total = data['TotalCount']
	issuetypes = data['Collection']
	issuetypes = {id_['IssueTypeID']: id_['IssueTypeName'] for id_ in issuetypes}
	assert(total == len(issuetypes))

	return issuetypes


# Trim to neccessary columns, apply human-readable labels, and then filter tickets for the morning post
def process_tickets(tickets:pd.DataFrame) -> pd.DataFrame:
	# Filter down to needed columns
	columns = ['IssueNumber', 'SubmittedDate', 'Subject', 'IssueTypeID',
			   'AssignedTo', 'SubStatusID', 'RequiredByDate']
	tickets = tickets.loc[:, tickets.columns.intersection(columns)]

	# Apply proper labels to SubStatusID
	substatuses = get_substatuses()
	tickets.loc[:, 'SubStatusID'] = tickets['SubStatusID'].transform(lambda x: substatuses[x])	

	# Apply proper labels to IDs in IssueTypeID
	issuetypes = get_issuetypes()
	tickets.loc[:, 'IssueTypeID'] = tickets['IssueTypeID'].transform(lambda x: issuetypes[x])

	# Make AssignedTo uniform and make it work with Teams mentions (make it an email)
	make_email = lambda user: ''.join([user.lower(), '@auburn.edu'])
	tickets.loc[:, 'AssignedTo'] = tickets['AssignedTo'].transform(lambda x: make_email(x) if x is not None else 'None')

	# Select rows for morning post
	# Don't ping Adam. He's got this.
	tickets = tickets[tickets['IssueTypeID'] != 'Systems Administration'] 

	# Filter out paused tickets
	tickets = tickets[tickets['SubStatusID'].isin(['Unassigned', 'In Progress', 'Scheduled'])]
	
	return tickets


# Sort the tickets into the proper categories.
def sort_tickets(tickets:pd.DataFrame) -> dict[list[dict]]:
	# Get events
	events = tickets[tickets['IssueTypeID'] == 'Event']

	# Get scheduled that aren't events
	scheduled = tickets[tickets['SubStatusID'] == 'Scheduled']
	scheduled = scheduled[scheduled['IssueTypeID'] != 'Event']
	
	# Get miscellaneous tickets (those that aren't in the above two and weren't filtered in process_tickets()
	misc = tickets[tickets['SubStatusID'] != 'Scheduled']
	misc = misc[misc['IssueTypeID'] != 'Event']

	# Put into dictionary
	tickets = {}
	tickets['events'] = events.to_dict('records')
	tickets['scheduled'] = events.to_dict('records')
	tickets['misc'] = events.to_dict('records')

	return tickets


# Turns the list of dictionaries in sort_tickets into list of strings that'll be put into the morning post.
def format_tickets(tickets: dict[list[dict]]) -> dict[list[str]]:

	pass


# Create the necessary html string for posting in Teams
def render_post() -> str:

	pass

# 'Script' that this script achieves
def main():
	# Get necessary info
	tickies = get_tickets()
	categories = get_categories()
	schedule = get_schedule()

	# Process and sort tickets
	tickies = process_tickets(tickies)
	tickie_dict = sort_tickets(tickies)
	print(tickies)


	# Generate the post
	post = render_post()

	# Print the post for copying
	print(post)


if __name__ == '__main__':
	main()
