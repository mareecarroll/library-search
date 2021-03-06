"""
Provides functionality to search libraries in Melbourne area.

Returns results as SearchResult named tuple with library and title attributes.
"""
import sys
import requests
from bs4 import BeautifulSoup 
from collections import namedtuple
from configparser import ConfigParser
from os.path import dirname, realpath, join
import urllib


# config = ConfigParser()
# config.read(join(dirname(realpath(__file__)), '.env'))


SearchResult = namedtuple("SearchResult", "library title")
"""
SearchResult named tuple structure for holding search result details

So far the attributes are:
- library (str): the name of the library catalogue result is from
- title (str): the search result entry including book title

To do:
- parse search result to extract title and author, possibly ISBN
"""


def search_yarra(search_term):
    """
    Searches Yarra libraries catalogue.

    Args:
        search_term (str): The search term for the library catalogue search
    Returns:
        (list of SearchResult named tuple): The search results
    """
    library = 'yarra'
    payload = {'qu': search_term }
    url = 'https://coyl.swft.ent.sirsidynix.net.au/client/en_AU/coylnow/search/results'
    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = []
    for div in soup.find_all("div", {"class": "displayDetailLink"}):
        titles.append(SearchResult(library=library, title=div.find('a').get('title')))
    return titles


def search_melbourne(search_term):
    """
    Searches Melbourne libraries catalogue.

    Args:
        search_term (str): The search term for the library catalogue search
    Returns:
        (list of SearchResult named tuple): The search results
    """
    library = 'melbourne'
    url = 'https://librarysearch.melbourne.vic.gov.au/cgi-bin/spydus.exe/ENQ/OPAC/BIBENQ'
    payload = {
            'ENTRY':search_term,
            'ENTRY_NAME':'BS',
            'ENTRY_TYPE':'K',
            'SEARCH_FORM':'/cgi-bin/spydus.exe/MSGTRN/OPAC/BSEARCH?HOMEPRMS=BSEARCHPARAMS',
            'SORTS':'SQL_REL_TITLE',
            'ISGLB':'0',
            'GQ':search_term
    }
    referer = 'https://librarysearch.melbourne.vic.gov.au/cgi-bin/spydus.exe/MSGTRN/OPAC/HOME'
    r = requests.get(url, params=payload, headers={'referer': referer})
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = []
    for ul in soup.find_all("ul", {"class": "briefRecords"}):
        for li in ul.find_all('li'):
            for a in li.find_all('a')[2:3]:
                titles.append(SearchResult(library=library, title=a.text))
    return titles


def search_moreland(search_term):
    """
    Searches Moreland libraries catalogue.

    Args:
        search_term (str): The search term for the library catalogue search
    Returns:
        (list of SearchResult named tuple): The search results
    """
    library = 'moreland'
    url = 'https://moreland.hosting.libero.com.au/libero/WebOpac.cls'
    referer = 'https://moreland.hosting.libero.com.au/libero/WebopacOpenURL.cls'
    payload = { 'MGWCHD':'0',
    'TOKEN':'0Oqurannvu4411',
    'TOKENX':'0Oqurannvu4411',
    'DATA':'MOR',
    'usercode':'',
    'VERSION':'2',
    'TERM_1': search_term,
    'USE_1':'ku',
    'PREFER':'0',
    'PSIZE':'30',
    'SimpSearch':'SIMPLESEARCH',
    'ACTION':'SEARCH' }
    r = requests.get(url, params=payload, headers={'referer': referer})
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = []
    for span in soup.find_all("span", {"class": "ShortTitleAv"}):
        for a in span.find_all('a')[0:1]:
            titles.append(SearchResult(library=library, title=a.text))
    return titles

def search_cloudlibrary_melbourne(search_term):
    """
    Searches Melbourne cloud library catalogue.

    Args:
        search_term (str): The search term for the library catalogue search
    Returns:
        (list of SearchResult named tuple): The search results
    """
    library = 'cloud library melbourne'
    data = {'SearchString': search_term, 'SortBy':"",'count':20,'from':0}
    payload = {'media': 'all', 'src': 'lib'}
    search_term = urllib.parse.quote(search_term)
    url = 'https://ebook.yourcloudlibrary.com/uisvc/melbourne/Search/CatalogSearch'
    referer = 'https://ebook.yourcloudlibrary.com/library/melbourne/Search/{}'.format(search_term)
    r = requests.post(url, params=payload, data=data, headers={'referer': referer})
    response = r.json()
    titles = []
    for item in response['Items']:
        last, first = item['Authors'].split(',')[0:2] # assuming only one author
        titles.append(SearchResult(library=library, 
                                   title="{} by {} {}".format(item["Title"], first, last)))
    return titles

def search_libraries(search_term):
    """
    Searches all library catalogues (Yarra, Melbourne, Moreland).

    Args:
        search_term (str): The search term for the library catalogues search
    Returns:
        (list of SearchResult named tuple): The search results zipped so that 
            the first result from each library catalogue appears 
            before the second result of any catalogue, etc
    """
    titles = []
    zipped = zip(search_yarra(search_term), 
                 search_melbourne(search_term), 
                 search_moreland(search_term),
                 search_cloudlibrary_melbourne(search_term))
    for yarra, melb, moreland, cloud_library_melb in zipped:
        titles.append(yarra)
        titles.append(melb)
        titles.append(moreland)
        titles.append(cloud_library_melb)
    return titles


def main():
    """Used if called as script from command line."""
    search_term = sys.argv[1]
    print(search_libraries(search_term))


if __name__ == "__main__":
    main()