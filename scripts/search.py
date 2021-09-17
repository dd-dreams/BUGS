import requests
from constants.other import SEARCH_URL


class Search:
    def __init__(self, artist, song, url=None):
        """
        constructor

        :param artist:
        :param song:
        :param url:
        """
        self.artist = artist
        self.song = song
        self.url = url
        self.request = requests.get(url) if url is not None else None

    def get_html(self):
        """
        returns the html after sending a request
        :return: source code of self.request if we requested else false
        """
        return self.request.text if self.request is not None else False

    def search(self, page=1):
        self.url = SEARCH_URL.format(page) + self.song + ' ' + self.artist
        self.request = requests.get(self.url)

    def get_song_html(self):
        """
        after searching, get the song source code
        the url needs to be updated to the song url
        :return:
        """
        self.request = requests.get(self.url)

    def update_url(self, url):
        self.url = url

    def get_url(self):
        return self.url
