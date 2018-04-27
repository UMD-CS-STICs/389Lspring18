import json
import os.path

def main(filename, output_filename):
    """Generates a JSON object for each faculty member with name, username, and URL."""
    if not os.path.isfile(filename):
        raise Exception(filename + ' does not exist.')
    with open(filename, 'r') as f:
        faculty = [{
            'name': line.split('\t')[0].strip(),
            'url': 'http://www.cs.umd.edu' + line.split('\t')[1].strip(),
            'username': line.split('\t')[1].strip()[len('/people/'):],
        } for line in f.readlines()]

        with open(output_filename, 'w') as out:
            json.dump(faculty, out, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    SCRAPED_FACULTY_FILE = "data/scraped-faculty.txt"
    FACULTY_FILE = 'data/faculty-data.json'

    main(SCRAPED_FACULTY_FILE, FACULTY_FILE)
