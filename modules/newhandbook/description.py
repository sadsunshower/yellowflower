# Code by Nicc
# YellowFlower

# Utility file for Handbook module, scrapes and processes course descriptions

import bs4, requests

from modules.newhandbook.info import HandbookDetails


def soup_parse_string(tag: bs4.element.Tag) -> str:
    ret = ''

    for string in tag.strings:
        stripped = string.strip()
        if stripped != '':
            stripped += '\n'

        ret += stripped
    
    return ret


def soup_parse_courses(root_tag: bs4.element.Tag) -> str:
    ret = []
    for tag in root_tag.children:
        if isinstance(tag, bs4.NavigableString):
            continue

        course = ''
        for string in tag.strings:
            if string == 'arrow_forward' or 'UOC' in string:
                continue
            
            stripped = string.strip()
            if stripped != '':
                stripped += ' '
            
            course += stripped

        ret.append(course)
    
    return '; '.join(ret)


def fetch_description(year: int, course_code: str) -> HandbookDetails:
    course_description = {
        'code' : course_code,
        'url' : f'https://www.handbook.unsw.edu.au/undergraduate/courses/{year}/{course_code}'
    }

    url = f'https://www.handbook.unsw.edu.au/undergraduate/courses/{year}/{course_code}'

    page_ug = requests.get(f'https://www.handbook.unsw.edu.au/undergraduate/courses/{year}/{course_code}')

    if page_ug.status_code != 200:
        return None
    
    soup = bs4.BeautifulSoup(page_ug.text, features='lxml')

    tag_description = soup.findAll('div', {'class' : 'readmore__wrapper'})[0]
    description = soup_parse_string(tag_description)

    tag_title = soup.findAll('span', {'data-hbui' : 'module-title'})[0]
    title = soup_parse_string(tag_title)
    
    offering = f'Not offered in {year} or offerings not up-to-date.'
    
    if soup.find('strong', string='Offering Terms'):
        tag_offering = list(soup.find('strong', string='Offering Terms').parent.children)[3]
        offering = soup_parse_string(tag_offering)
    
    conditions = None

    if soup.find('div', id='readMoreSubjectConditions'):
        tag_conditions = list(soup.find('div', id='readMoreSubjectConditions').children)[1]
        conditions = soup_parse_string(tag_conditions)
    
    equivalent = None

    if soup.find('h3', string='Equivalent Courses'):
        tag_equivalent_root = list(soup.find('h3', string='Equivalent Courses').parent.children)[3]
        equivalent = soup_parse_courses(tag_equivalent_root)
    
    exclusion = None

    if soup.find('h3', string='Exclusion Courses'):
        tag_exclusion_root = list(soup.find('h3', string='Exclusion Courses').parent.children)[3]
        exclusion = soup_parse_courses(tag_exclusion_root)

    return HandbookDetails(course_code, url, title, description, offering, conditions, equivalent, exclusion)


# Interactive console for debugging
if __name__ == '__main__':
    while True:
        code = input('Course code: ')
        print(fetch_description(2020, code.upper()))