# tools to extract search data from linked urls
from typing import List, Tuple
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from typing import NamedTuple
import json
import re

from haystack.utils.highlighting import Highlighter


class PhraseHighlighter(Highlighter):
    """
    Haystack's Highlighter class is designed to highlight words, not phrases.
    This class extends the Highlighter class to highlight phrases.
    """

    def __init__(self, query, **kwargs):
        super().__init__(query, **kwargs)

        # extract all phrases in self.query that are surrounded by double quotes
        # and add them to self.query_words (a set)
        phrases = re.findall(r'"([^"]*)"', self.query)
        self.query_words.update(phrases)

        # remove search operators like AND, OR, NOT from self.query_words
        banned = ["AND", "OR", "NOT"]
        self.query_words = {
            word for word in self.query_words if word.upper() not in banned
        }


class SearchData(NamedTuple):
    url: str
    text: str
    title: str = ""


def get_data_from_mysociety_blog(url: str, title: str) -> List[SearchData]:
    """
    parse a mysociety blog url, return the main content of the article,
    and creates a list of URL, content pairs.
    The URL is a deep link to the paragraph using chrome's deep linking syntax.
    This is : #:~:text=url%20encoded%20text
    """
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # The main content is in the 'wordpress-editor-content' div, we want each individual paragraph
    # so we can link to them
    content = soup.find("div", {"class": "wordpress-editor-content"})
    paragraphs = content.find_all("p")

    for p in paragraphs:
        # get the text of the paragraph
        text = p.get_text().strip()
        # create a deep link to the paragraph
        link = url + "#:~:text=" + parse.quote(text[:800])
        # add the link and text to the list
        if text:
            items.append(SearchData(url=link, text=text, title=title))

    return items


def get_stringprint_search_data(url: str, title: str) -> List[SearchData]:
    """
    Stringprint stores the search data in a js file (/tipuesearch_content.js).
    Extract this, do light rearrangement to get the json.
    """

    # construct the search url. The base url may end in a slash (base directory)
    # if it is a file, we want to append the search file to the base directory.
    # if it is a directory, we want to append the search file to the base url.
    if url.endswith("/"):
        search_url = url + "tipuesearch_content.js"
    else:
        base_directory = url.split("/")[:-1]
        search_url = "/".join(base_directory) + "/tipuesearch_content.js"
    html = request.urlopen(search_url).read()
    html = html.replace(b"var tipuesearch = ", b"").strip()[:-1]
    data = json.loads(html)
    items = []
    for item in data["pages"]:
        # item url looks like index.html#1.1.skd7w.ynn0e.ddb6c.5asoj
        # if the base url ends in a slash, we want to append the item url.
        # if it is a full html path, we want to add the hash after the base url.
        if url.endswith("/") and "index.html" not in item["url"]:
            link = url + item["url"]
        else:
            # extract just the hash from the item url
            link = url + "#" + item["url"].split("#")[1]

        # if there is an item title, append it with a colon after the base title
        if item["title"]:
            item_title = title + ": " + item["title"]
        else:
            item_title = title

        text = item["text"].strip()

        if text:
            items.append(SearchData(url=link, text=text, title=item_title))
    return items
