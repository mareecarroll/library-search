from search_libraries import *

def test_search_yarra():
    search_results = search_yarra("the book of phoenix")
    assert len(search_results) > 0, "Expected at least one result"
    assert all(isinstance(x, SearchResult) for x in search_results), \
        "Expected all items in list to be SearchResult type"


def test_search_melbourne():
    search_results = search_melbourne("the book of phoenix")
    assert len(search_results) > 0, "Expected at least one result"
    assert all(isinstance(x, SearchResult) for x in search_results), \
        "Expected all items in list to be SearchResult type"

def test_search_moreland():
    search_results = search_moreland("the book of phoenix")
    assert len(search_results) > 0, "Expected at least one result"
    assert all(isinstance(x, SearchResult) for x in search_results), \
        "Expected all items in list to be SearchResult type"


