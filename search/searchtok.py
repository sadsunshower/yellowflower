import json, re

# course database
courses = {}
with open('courses.json', 'r') as f:
	courses = json.loads(f.read())

i = 0
for area in courses:
    for course in courses[area]['courses']:
        c_tokens = [course.lower()[:4]]
        c_tokens += list(filter(lambda x: len(x) > 1, re.split(r'\W', courses[area]['courses'][course].lower())))

        print(course + ' ' + courses[area]['courses'][course] + '|' + '|'.join(c_tokens))
        
        i += 1