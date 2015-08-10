from bs4 import BeautifulSoup
import urllib

def list_of_links(tag):
  return tag.name == "a" and tag.parent.name == "li"

def list_of_links_all_seasons(tag):

  return tag.name == "a" and tag.parent.name == "li" and "season" in tag.string.lower()
def link_with_next_sibling_string(tag):
  return tag.name == "a" \
    and not "style" in tag.attrs \
    and len(tag.find_parents("table"))

def links_with_nofollow_and_no_style_with_img(tag):
  return tag.name == "a" \
    and "rel" in tag.attrs \
    and tag.attrs["rel"][0] == "nofollow" \
    and not "style" in tag.attrs \
    and tag.contents \
    and tag.contents[0].name == "img"

def link_with_input_value(tag):
  return tag.name == "a" \
    and "rel" in tag.attrs \
    and tag.attrs["rel"][0] == "nofollow" \
    and tag.contents[0].attrs["value"].lower() == "continue to video"

def get_html_soup(url, function):
  handle = urllib.urlopen(url)
  doc = handle.read()
  soup = BeautifulSoup(doc, 'html.parser')
  return soup.find_all(function)

