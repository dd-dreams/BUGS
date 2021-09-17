#!/usr/bin/python3

from termcolor import colored
import scraper
import chords
import search
import sys
from colorama import init
import argparse
from constants.messages import *
from constants.other import CACHED_SITES
import os
import webbrowser
import json

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
    if os.path.isfile(path.replace(" ", "_")):
        webbrowser.open(path.replace(" ", "_"))
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


def clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def complex(search_obj):
    """
    complex mode TODO: Add better doc

    :return:
    """
    inp = ""
    suggestions = []
    while inp not in suggestions:
        inp = input("Search (Enter for search results): ")
        if inp.isdigit() and len(suggestions) > 0:
            if int(inp) - 1 > len(suggestions) - 1 or int(inp) - 1 < 0:
                print_status("Search result does not exist (index out of bounds)", "red")
                continue
            return suggestions[int(inp) - 1]
        clear()
        search_obj.update_song(inp)
        suggestions = search_obj.suggestions()
        if "403" in suggestions:  # it means the user inputted an exact song name, or there are no results
            print_status(SONGS_NOT_FOUND, "red")
            continue
        suggestions = json.loads(suggestions)["suggestions"]
        for ind, suggestion in enumerate(suggestions, start=1):
            print_status(f"[{ind}] {suggestion}")
    print()
    return inp


def scrape(scraper_obj):
    """
    this func will be executed when the user chose to scrape the site
    meaning if he want to get the search results by specifying
    song and artist.

    :return:
    """
    if scraper_obj.get_song() is None and scraper_obj.get_artist() is None:
        print_status(NO_SONG_OR_ARTIST, ERROR_COLOR)
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
    parser.add_argument('-c', '--complex', help="Complex mode. Adding search suggestions", action="store_true")
    args = parser.parse_args()

    # if no args supplied, display help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    try:
        artist = ""
        song = ""
        if args.artist is not None:
            artist = args.artist
        if args.song is not None:
            song = args.song
        if args.complex:
            search = search.Search()
            song = complex(search)
        scrap = scraper.Scraper(artist, song, args.url)
        if scrape(scrap) is False:
            sys.exit(0)
        if args.open:
            open_command(get_path_current_song(scrap.get_song()))
    except KeyboardInterrupt:
        print("\nBye")
