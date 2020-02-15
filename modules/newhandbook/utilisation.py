# Code by Nicc
# YellowFlower

# Utility file for Handbook module, scrapes and processes class utilisation data

import re, requests, typing


def parse_class(class_line: str) -> typing.Dict[str, int]:
    try:
        cells = [re.sub(r'</?td[^>]*>', r'', x).strip() for x in re.findall(r'<td[^>]*>[^<]*</td>', class_line)]

        return {
            'type' : cells[0],
            'name' : cells[1],
            'code' : cells[2],
            'status' : cells[4],
            'enrolled' : cells[5].split('/')[0],
            'capacity' : re.sub(r' \[[^\]]*\]', r'', cells[5].split('/')[1])
        }
    except Exception as e:
        return None


def fetch_utilisation(term: str, course_code: str) -> typing.List[typing.Dict[str, int]]:
    page = requests.get(f'http://classutil.unsw.edu.au/{course_code[:4]}_{term}.html')

    if page.status_code != 200:
        return None
    
    lines = page.text.split('\n')
    data_lines = []

    line_pointer = 0
    while course_code not in lines[line_pointer] or 'cucourse' not in lines[line_pointer]:
        line_pointer += 1
    
    line_pointer += 2
    
    while 'cucourse' not in lines[line_pointer]:
        data_lines.append(lines[line_pointer])
        line_pointer += 1

    classes = [parse_class(x) for x in data_lines if '&nbsp;&nbsp;' in x]

    return classes


# Interactive console for debugging
if __name__ == '__main__':
    while True:
        code = input('Course code: ')
        term = input('Term: ')
        print(fetch_utilisation(term.upper(), code.upper()))