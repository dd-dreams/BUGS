import requests
from constants.other import SEARCH_URL, SUGGESTIONS_URL
from fake_headers import Headers


class Search:
    def __init__(self, song="", url=None):
        """
        constructor

        :param artist:
        :param song:
        :param url:
        """
        self.song = song
        self.url = url
        self.headers = Headers(headers=True).generate()
        self.request = requests.get(url, headers=self.headers) if url is not None else None

    def request_url(self):
        return requests.get(self.url, headers=self.headers)

    def get_html(self):
        """
        returns the html after sending a request
        :return: source code of self.request if we requested else false
        """
        return self.request.text if self.request is not None else False

    def search(self, page=1):
        self.url = SEARCH_URL.format(page) + self.song
        self.request = self.request_url()

    def suggestions(self):
        """
        receiving suggestions

        :return:
        """
        self.url = SUGGESTIONS_URL.format(self.song[0], self.song)
        self.request = self.request_url()
        return self.request.text

    def get_song_html(self):
        """
        after searching, get the song source code
        the url needs to be updated to the song url
        :return:
        """
        self.request = self.request_url()

    def update_url(self, url):
        self.url = url

    def update_song(self, update):
        self.song = update

    def get_url(self):
        return self.url

