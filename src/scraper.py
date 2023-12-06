#!/usr/bin/python

from termcolor import colored
import json
from bs4 import BeautifulSoup
from constants.html_classes import HTML_DATA
import search


class Scraper:
    def __init__(self, song, url=None):
        """
        Constructor

        :param song: specified song
        :param url: url song, by default None and will try to search for the song
        """
        self.__elements = []
        self.song = song
        self.data = None
        self.search_results = None
        self.search = search.Search(song, url)
        self.final_url = url
        self.re_soup = lambda: BeautifulSoup(self.search.get_html(), "lxml") if self.search.get_html() else None
        self.__soup = self.re_soup()
        self.chords = None

    def get_search_results(self, page=1):
        """
        method to scrape the search results
        :return: list(search results)
        """
        self.search.search(page)
        self.__soup = self.re_soup()
        try:
            content = self.__soup.find("div", class_=HTML_DATA).attrs['data-content']
            self.search_results = json.loads(content)['store']['page']['data']['results']
            self.remove_paid()
        except AttributeError:
            return False
        return self.search_results

    def remove_paid(self):
        """
        method for removing paid tabs

        :return:
        """
        no_paid_list = []
        for result in self.search_results:
            if 'marketing_type' in list(result.keys()):
                continue
            no_paid_list.append(result)
        self.search_results = no_paid_list

    def get_info(self):
        """
        get the info from the above url such as the chords or rating AFTER you searched and chose
        a song
        :return: json object with the info
        """
        if self.final_url is None:
            return False
        self.search.update_url(self.final_url)
        self.search.get_song_html()
        self.__soup = self.re_soup()
        content = self.__soup.find("div", class_=HTML_DATA).attrs['data-content']
        self.data = json.loads(content)['store']['page']['data']['tab_view']
        return self.data

    def get_chords(self):
        """
        get the chords

        :return: chords if self.data is not none else false
        """

        self.chords = self.data['wiki_tab']['content']
        return self.chords

    def print_results(self):
        songs = " " * 6
        for index, song in enumerate(self.search_results):
            songs += colored(f"[{index + 1}] ", 'yellow') + colored(f"Artist: {song['artist_name']},"
                                                                    f" {song['song_name']}"
                                                                    f", Rating: {song['votes']}, "
                                                                    f"{song['type']}\n", 'red')
            songs += " " * 6
        print(songs)

    def set_final_url(self, index):
        """
        settings the final url, after choosing the song you want to get the chords from
        :return:
        """
        self.final_url = self.search_results[index]['tab_url']

    def get_data(self):
        """
        get the data

        :return: data
        """
        return self.data

    def get_song(self):
        return self.song

    def get_final_url(self):
        return self.final_url

    def update_song(self, update):
        """
        this method is used when receiving suggestions (complex mode is on)

        :param update:
        :return:
        """
        self.song = update
