# code by nicc
# yellowflower

# module: handbook
# scrapes the UNSW handbook for course information

import asyncio

import bs4
import requests

import json, re, subprocess


# course database
courses = {}
with open('search/courses.json', 'r') as f:
	courses = json.loads(f.read())


# requests a bs4 object from a url
def load_page(url):
	full_url = 'https://www.handbook.unsw.edu.au/undergraduate/' + url
	page = requests.get(full_url)

	print('handbook: DEBUG: url ' + full_url + '...')

	if page.status_code != 200:
		full_url = 'https://www.handbook.unsw.edu.au/postgraduate/' + url
		page = requests.get(full_url)

		print('handbook: DEBUG: url ' + full_url + '...')

		if page.status_code != 200:
			return None, None

	soup = bs4.BeautifulSoup(page.text, features='lxml')

	return soup, full_url


# gets the details of a subject as an object
async def subject_details(code):
	code = re.sub(r'[^A-Z0-9]', '', code.upper())

	soup, full_url = load_page('courses/2019/' + code)

	if soup is None:
		return None

	course_title = re.sub(r'^\s+|\s+$', '', soup.find('span', attrs={'data-hbui' : 'module-title'}).string)

	course_offerings_tag = soup.find('strong', string=re.compile('Offering Terms'))

	course_offerings = 'None'

	if course_offerings_tag:
		course_offerings = re.sub(r'^\s+|\s+$', '', course_offerings_tag.parent.contents[3].string)

	course_conditions_tag = soup.find('div', id='readMoreSubjectConditions')

	course_conditions = ''

	if course_conditions_tag:
		for string in course_conditions_tag.contents[1].contents[1].strings:
			course_conditions += string
	else:
		course_conditions = 'None'

	course_conditions = re.sub(r'^\s+|\s+$', '', course_conditions)

	course_description_tag = soup.find('div', id='readMoreIntro')

	course_description = ''

	if len(course_description_tag.contents[1].contents) > 1 and course_description_tag.contents[1].contents[1].name == 'p':
		for string in course_description_tag.contents[1].contents[1].strings:
			course_description += string
	else:
		course_description = course_description_tag.contents[1].contents[0].string

	course_description = re.sub(r'^\s+|\s+$', '', course_description)

	return {
		'title' : course_title,
		'description' : course_description,
		'offerings' : course_offerings,
		'conditions' : course_conditions,
		'link' : full_url
	}


# determines what the user was requesting (course / program / specialisation) and returns appropriate details
async def handle_query(query):
	if re.search(r'^[a-zA-Z]{4}[0-9]{4}$', query):
		return await subject_details(query)
	else:
		return None


# string distance utility function
# just use the one from wikipedia
def levenshtein_damerau(s1, s2):
	cost = 0

	if len(s1) == 0:
		return len(s2)
	if len(s2) == 0:
		return len(s1)
	
	if s1[-1] == s2[-1]:
		cost = 0
	else:
		cost = 1

	other = 100000
	if len(s1) > 1 and len(s2) > 1 and s1[-2] == s2[-1] and s1[-1] == s2[-2]:
		other = levenshtein_damerau(s1[:-2], s2[:-2]) + cost

	return min([
		levenshtein_damerau(s1[:-1], s2) + 1,
		levenshtein_damerau(s1, s2[:-1]) + 1,
		levenshtein_damerau(s1[:-1], s2[:-1]) + cost,
		other
	])


# search the "handbook" by actually searching our internal database
async def handbook_search(query):
	if re.search(r'^[0-9]{4}$', query):
		results = {}

		i = 0
		for area in courses:
			for course in courses[area]['courses']:
				d = levenshtein_damerau(course[4:], query)
				results[course + ' ' + courses[area]['courses'][course]] = d
		
		displayed_results = list(filter(lambda x: results[x] < 2, results.keys()))
		displayed_results.sort(key=lambda x: results[x])
		
		return displayed_results
	elif re.search(r'^[0-9]{4}[a-z]{4}', query.lower()):
		results = {}

		i = 0
		for area in courses:
			for course in courses[area]['courses']:
				d = levenshtein_damerau(course.lower(), query.lower())
				results[course + ' ' + courses[area]['courses'][course]] = d
		
		displayed_results = list(filter(lambda x: results[x] < 3, results.keys()))
		displayed_results.sort(key=lambda x: results[x])
		
		return displayed_results
	else:
		q_tokens = list(filter(lambda x: len(x) > 0, re.split(r'\W', query.lower())))
		print('query tokens: ' + ' '.join(q_tokens))
		results = {}

		if re.search(r'^[a-z]{4}$', query.lower()):
			for area in courses:
				for course in courses[area]['courses']:
					d = levenshtein_damerau(course[:4].lower(), query.lower())
					results[course + ' ' + courses[area]['courses'][course]] = d

		for i in range(len(q_tokens)):
			q_tokens[i] = re.sub(r'[^A-Za-z0-9-:]', '', q_tokens[i])
		
		search_ldd = subprocess.run(['./search/search_ldd'] + q_tokens, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

		for result in search_ldd:
			pair = result.split('|')
			if len(pair) < 2:
				break
			results[pair[0]] = int(pair[1])
		
		intermediate = list(results.keys())
		intermediate.sort(key=lambda x: results[x])

		return intermediate
		
		search_final = subprocess.run(['./search/combine'], input='\n'.join(intermediate).encode('utf-8', 'ignore'), stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
		return search_final