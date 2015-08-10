import config
import souphelpers as soup
import re
import urllib

ROOT = config.ROOT
SHOWS = ROOT + config.PATH

class Stream:
  def __init__(self, url):
    self.url = url

class Provider:
  def __init__(self, name):
    self.name = name
    self.urls = [] # offsite links
    self.streams = []

  def get_streams(self):
    print "get_stream: %s" % self.name
    for url in self.urls:
      handle = urllib.urlopen(url)
      doc = handle.read()
      match = re.search(r'(htt[ps]://.+\.mp4)', doc)
      if match:
        self.streams.append(Stream(match.group(0)))
      else:
        print "No mp4 found: %s" % url

  def __str__(self):
    return self.name
    
  def __repr__(self):
    return self.name

class Episode:
  def __init__(self, name, url):
    self.name = name
    self.url = url
    self.episode = None
    self.providers = {}

  def get_providers(self):
    if not self.providers:
      soup_list = soup.get_html_soup(self.url, soup.links_with_nofollow_and_no_style_with_img)
      for provider in soup_list:
        domain, url = provider.contents[0].string.strip(), provider.attrs["href"]
        if not domain in self.providers:
          self.providers[domain] = Provider(domain)
        soup_list2 = soup.get_html_soup(url, soup.link_with_input_value)
        offsite_url = soup_list2[0].attrs["href"]
        self.providers[domain].urls.append(offsite_url)
    return self.providers

  def __str__(self):
    return self.name
    
  def __repr__(self):
    return self.name



class Season:
  def __init__(self, name, url):
    self.name = name
    self.url = url
    self.season = None
    self.episodes = {}

  def get_episodes(self):
    if not self.episodes:
      soup_list = soup.get_html_soup(self.url, soup.link_with_next_sibling_string)
      for episode in soup_list:
        new_episode = Episode(episode.string, episode.attrs["href"])
        self.episodes[new_episode.name] = new_episode
    return self.episodes

  # Not guaranteed to be correct
  def get_episode(self, episode):
    self.get_episodes()
    if episode > 0 and episode <= len(self.episodes):
      selected_episode = self.episodes[episode - 1]
      return selected_episode
    else:
      return None

  def __str__(self):
    return self.name
    
  def __repr__(self):
    return self.name



class Show:
  def __init__(self, name, url):
    self.name = name
    self.url = url
    self.seasons = {}

  def get_seasons(self):
    if not self.seasons:
      soup_list = soup.get_html_soup(self.url, soup.list_of_links_all_seasons)
      for season in soup_list:
        new_season = Season(season.string, season.attrs["href"])
        self.seasons[new_season.name] = new_season
    return self.seasons

   # Not guaranteed to be correct
   def get_season(self, season):
    self.get_seasons()
    if season in self.seasons:
      return self.seasons[season]
    else:
      return None

  def __str__(self):
    return self.name

  def __repr__(self):
    return self.name

class PFTV:
  def __init__(self):
    self.shows = {}

  # Populate List
  def get_shows(self):
    if not self.shows:
      soup_list = soup.get_html_soup(SHOWS, soup.list_of_links)
      for show in soup_list:
        new_show = Show(show.attrs["title"], show.attrs["href"])
        self.shows[new_show.name] = new_show
    return self.shows

  def get_show(self, name):
    self.get_shows()
    return self.shows[name]

  # Search
  def search(self, name):
    self.get_shows()
    results = {}
    for key in self.shows.keys():
      if name not in key.lower(): 
        continue
      results[key.strip()] = self.shows[key.strip()]
    return results

  def __str__(self):
    return "PFTV"

  def __repr__(self):
    return "PFTV"

