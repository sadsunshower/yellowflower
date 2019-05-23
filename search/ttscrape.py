import requests

import json, re, time

home = requests.get('http://timetable.unsw.edu.au/2019/subjectSearch.html')
lines = home.text.split('\n')

pair = False
last = ''
entries = {}

for line in lines:
    if re.search(r'class="data"', line) and re.search(r'a href="[^#]', line):
        addr = re.search(r'href="([^"]*)"', line).group(1)
        line = re.sub(r'^\s+', '', line)
        line = re.sub(r'<[^>]*>', '', line)
        line = re.sub(r'&amp;', '&', line)
        if pair:
            entries[last] = {
                'name': line,
                'addr': addr,
                'courses': {}
            }
        else:
            last = line

        pair = not pair

del entries['By Teaching Period']

def courseFill(subj):
    global entries

    time.sleep(3)
    page = requests.get('http://timetable.unsw.edu.au/2019/' + entries[subj]['addr'])
    lines = page.text.split('\n')
    
    pair = False
    last = ''

    for line in lines:
        if re.search(r'class="data"', line) and re.search(r'a href="[^#]', line):
            line = re.sub(r'^\s+', '', line)
            line = re.sub(r'<[^>]*>', '', line)
            line = re.sub(r'&amp;', '&', line)
            if pair:
                entries[subj]['courses'][last] = line
            else:
                last = line

            pair = not pair

    del entries[subj]['courses']['New search by Campus/Subject Area']

for subj in entries:
    print('filling out', subj)
    courseFill(subj)

with open('courses.json', 'w') as f:
    f.write(json.dumps(entries))