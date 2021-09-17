#!/usr/bin/python3

from termcolor import colored
import scraper
import chords
import sys
from colorama import init
import argparse
from constants.messages import *
from constants.other import CACHED_SITES
import os
import webbrowser

ERROR_COLOR = colored("[!]", 'red')
SUCCESS_COLOR = colored("[*]", 'blue')


def print_status(text, status=None):
    """
    prints colored texts
    """
    if status is None:
        print(SUCCESS_COLOR, colored(text, 'yellow'))
    else:
        print(ERROR_COLOR, colored(text, 'yellow'))


def open_command(path):
    if os.path.isfile(path):
        webbrowser.open(path)
    else:
        print_status(FILE_NOT_EXIST, ERROR_COLOR)


def choose_song(scraper_obj):
    scraper_obj.print_results()
    chosen = input("Choose song (Enter for next page): ")
    return chosen


def check_in_cache(name):
    name += ".html"
    file = os.path.join(CACHED_SITES, name)
    return os.path.isfile(file)


def scrape(scraper_obj):
    """
    this func will be executed when the user chose to scrape the site
    meaning if he want to get the search results by specifying
    song and artist.

    :return:
    """
    if scraper_obj.get_song() is None:
        print_status(NO_SONG_SET, ERROR_COLOR)
        return False
    if scraper_obj.get_artist() is None:
        print_status(NO_ARTIST_SET, ERROR_COLOR)
        return False
    if scraper_obj.get_final_url() is None:
        print_status(FETCHING_RESULTS)
        if len(scraper_obj.get_search_results()) == 0:
            print_status(SONGS_NOT_FOUND)
            return False
        print_status(SUCCESS_SCRAPE)
        print_status(SONGS_FOUND)
        page = 1
        chosen_song = choose_song(scraper_obj)
        while chosen_song == "":  # if the user chose to go to the next page
            page += 1
            if not scraper_obj.get_search_results(page):
                print_status("FINAL PAGE", "red")
                page -= 1
            chosen_song = choose_song(scraper_obj)
        chosen_song = int(chosen_song)
        scraper_obj.set_final_url(chosen_song)
    scraper_obj.get_info()
    final_chords = scraper_obj.get_chords()
    chords_obj = chords.Chords(scraper_obj.get_song(), scraper_obj.get_artist(), final_chords)
    print_status(OUTPUTTING_MSG)
    chords_obj.output_chords()
    print_status(SUCCESS_CHORDS)


def get_path_current_song(name):
    """
    this is a function to get the current path of the current song

    :return: path
    """
    path = f"{os.getcwd()}/{CACHED_SITES}/{name}.html"
    return path


if __name__ == '__main__':
    init()  # sometimes the colors do not appear good on some platforms, init() fix it
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--song', help="Provide song")
    parser.add_argument('-a', '--artist', help="Provide artist")
    parser.add_argument('-o', '--open', help="Open HTML file in browser after scraped", action="store_true")
    parser.add_argument('-u', '--url', help="Specific url to scrape from")
    args = parser.parse_args()

    # if no args supplied, display help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    try:
        scrap = scraper.Scraper(args.artist, args.song, args.url)
        if scrape(scrap) is False:
            sys.exit(0)
        if args.open:
            open_command(get_path_current_song(scrap.get_song()))
    except KeyboardInterrupt:
        print("\nBye")
