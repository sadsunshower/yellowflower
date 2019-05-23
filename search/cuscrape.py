import requests

import json, re, sys, time

codes = []
with open('subjcodes.txt', 'r') as f:
    lines = f.read().split('\n')
    for line in lines:
        codes.append(line)

courses = {}

def courseFill(subj):
    for term in range(1, 4):
        time.sleep(3)
        page = requests.get('http://classutil.unsw.edu.au/' + subj + '_T' + str(term) + '.html')
        if not page.text:
            continue

        lines = page.text.split('\n')

        curr_course = ''
        lecs = -1
        enrol = -1
        for line in lines:
            if re.search(r'class="cucourse"', line) and re.search(r'[A-Z]{4}[0-9]{4}', line):
                if lecs != -1:
                    courses[curr_course] = lecs
                else:
                    courses[curr_course] = enrol
                curr_course = re.search(r'[A-Z]{4}[0-9]{4}', line).group(0)
                lecs = -1
                enrol = -1
            elif re.search(r'<td>', line) and (re.search(r'LEC', line) or re.search(r'CRS', line)) and re.search(r'[0-9]+/[0-9]+', line):
                if re.search(r'LEC', line):
                    if lecs == -1:
                        lecs = 0
                    lecs += int(re.search(r'([0-9]+)/[0-9]+', line).group(1))
                elif re.search(r'CRS', line):
                    if enrol == -1:
                        enrol = 0
                    enrol += int(re.search(r'([0-9]+)/[0-9]+', line).group(1))

for subj in codes:
    print('filling ' + subj, file=sys.stderr)
    courseFill(subj)

for course in courses:
    print(course + '|' + str(courses[course]))