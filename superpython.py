#! /usr/bin/python3
import json
import re
import sys
import urllib.error
import urllib.request



def getSteps(data):
	sections = data['courses'][0]['sections']
	units = []

	for section_id in sections:
		section_link = 'https://stepik.org/api/sections/' + str(section_id)

		try:
			with urllib.request.urlopen(section_link) as url:
				res_section = json.loads(url.read().decode())
				units += res_section['sections'][0]['units']
		except urllib.error.HTTPError as e:
			print('\x1b[31m' + "Houston, we have a problem:" + '\x1b[0m', e.reason)

	print('\x1b[32m' + 'Getting lessons...' + '\x1b[0m')
	lessons = []

	for unit_id in units:
		unit_link = 'https://stepik.org/api/units?ids[]=' + str(unit_id)

		try:
			with urllib.request.urlopen(unit_link) as url:
				res_unit = json.loads(url.read().decode())
				lessons.append(res_unit['units'][0]['lesson'])
		except urllib.error.HTTPError as e:
			print('\x1b[31m' + "Houston, we have a problem:" + '\x1b[0m', e.reason)

	print('\x1b[32m' + 'Getting steps...' + '\x1b[0m')

	steps = []
	
	for lesson_id in lessons:
		lesson_link = 'https://stepik.org/api/lessons/' + str(lesson_id)

		try:
			with urllib.request.urlopen(lesson_link) as url:
				res_lesson = json.loads(url.read().decode())
				steps += res_lesson['lessons'][0]['steps']				
		except urllib.error.HTTPError as e:
			print('\x1b[31m' + "Houston, we have a problem:" + '\x1b[0m', e.reason)

	return steps
	



course_link = input('\x1b[36m' + 'The link, dude, say me the link (start with "https").' + '\x1b[0m\n')
pattern = '\s{0,4}https://stepik.org/course/(\d{1,10})/?\s{0,4}'
match = re.fullmatch(pattern, course_link) 

if not match:
	while not match:
		course_link = input('\x1b[31m' + 'It is the wrong sort of link.\n' +  '\x1b[0m' + '\x1b[36m' +'Give me a correct link or print "exit" for quit:' + '\x1b[0m\n')
		match = re.fullmatch(pattern, course_link)
		if course_link == "exit":
			sys.exit('\x1b[36m' + "It's the stop of executing. Bye-bye." + '\x1b[0m')


print('\x1b[36m' + 'Be patient, mortal, I\'m calculating...' + '\x1b[0m')	
course_id = re.search(pattern, course_link).group(1)
api_link = "https://stepik.org/api/courses/" + course_id

try:
	with urllib.request.urlopen(api_link) as url:
		data = json.loads(url.read().decode())
		step = getSteps(data)[1]
		print(step)
except urllib.error.HTTPError as e:
	print('\x1b[31m' + "Houston, we have a problem:" + '\x1b[0m', e.reason)
