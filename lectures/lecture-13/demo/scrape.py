import json
import os.path
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from requests.adapters import HTTPAdapter
import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_text(url):
    """https://stackoverflow.com/a/1983219/1935727

    This is a simple algorithm for scraping visible text from a webpage. You'd
    want to make this smarter if you actually were creating a real search engine.
    """
    print('Scraping: ' + url)

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    html = s.get(url)._content

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.find('section', {'aria-label': 'main content'}).findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    return u" ".join(t.strip() for t in visible_texts)

def scrape(name, url, username):
    text = get_text(url)

    return {
        'name': name,
        'url': url,
        'username': username,
        'text': text,
    }

def main(filename, output_filename):
    if not os.path.isfile(filename):
        raise Exception(filename + ' does not exist.')

    with open(filename, 'r') as f:
        results = []
        try:
            for faculty in json.loads(f.read())[24:]:
                results.append({
                    "index": {
                        "_index": "umdcs",
                        "_type": "faculty"
                    }
                })
                results.append(scrape(**faculty))
        finally:
            with open(output_filename, 'w') as out:
                for result in results:
                    json.dump(result, out, ensure_ascii=False)
                    out.write('\n')

if __name__ == '__main__':
    FACULTY_FILE = "data/faculty-data.json"
    FACULTY_SITE_FILE = "data/faculty-site-data.json"

    main(FACULTY_FILE, FACULTY_SITE_FILE)
