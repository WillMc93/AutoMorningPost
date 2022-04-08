import json
from datetime import datetime

import pandas as pd

from IssuetrakAPI import IssuetrakAPI


CATEGORIES_PATH = './categories.idk'
SEVENTEEN_SCHEDULE = './017_schedule.csv'


# Gather all tickets for the post.
def get_tickets() -> list:
	# Define the search request DTO/JSON
	request = {
		'Status': 'Open',
		'Deleted': 'false',
	}

	# Initialize API connection
	api = IssuetrakAPI()

	# Perform search
	response = api.perfromPost('/issues/search/', '', json.dumps(request))

	pass


# Get the categories w/ custom strings.
def get_categories(path:str=CATEGORIES_PATH) -> dict:

	pass


# Get the 017 schedule from file
def get_schedule(path:str=SEVENTEEN_SCHEDULE) -> dict:

	pass


# Sort the tickets into the proper categories.
def sort_tickets(tickets:list, categories:dict) -> dict:

	pass


# Create the necessary html string for posting in Teams
def render_post() -> str:

	pass


def main():
	# Get necessary info
	tickies = get_tickets()
	categories = get_categories()
	schedule = get_schedule()

	# Sort tickets into categories
	tickie_dict = sort_tickets(tickies, categories)

	# Generate the post
	post = render_post()

	# Print the post for copying
	print(post)

