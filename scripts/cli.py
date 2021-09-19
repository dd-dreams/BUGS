#!/usr/bin/python3

from termcolor import colored
import scraper
import chords
import search
import sys
import argparse
from constants.messages import *
from constants.other import CACHED_SITES, TMP
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


def open_command():
    if os.path.isfile(TMP):
        webbrowser.open(TMP)
    else:
        print_status(FILE_NOT_EXIST, ERROR_COLOR)


def choose_song(scraper_obj):
    scraper_obj.print_results()
    chosen = input("Choose song (Enter for next page): ")
    return chosen


def clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def complex(search_obj, starter):
    """
    complex mode TODO: Add better doc

    :param search_obj: search object
    :param starter: user most specify when using arguments the starting search
    :return:
    """
    search_obj.update_song(starter)
    suggestions = json.loads(search_obj.suggestions())["suggestions"]
    first = True  # is the first time the user searches
    while starter not in suggestions or len(suggestions) != 1:
        if "403" in suggestions:  # it means the user inputted an exact song name, or there are no results
            if first:
                return starter
            print_status(SONGS_NOT_FOUND, ERROR_COLOR)
            continue
        for ind, suggestion in enumerate(suggestions, start=1):
            print_status(f"[{ind}] {suggestion}")
        starter = input("Search (Enter for search results): ")
        if starter in suggestions:
            return starter
        if starter == "":
            print_status(NO_SEARCH, ERROR_COLOR)
            continue
        if starter.isdigit() and len(suggestions) > 0:
            if int(starter) - 1 > len(suggestions) - 1 or int(starter) - 1 < 0:
                print_status("Search result does not exist (index out of bounds)", "red")
                continue
            return suggestions[int(starter) - 1]
        clear()
        search_obj.update_song(starter)
        suggestions = json.loads(search_obj.suggestions())["suggestions"]
        first = False
    print()
    return starter


def scrape(scraper_obj):
    """
    this func will be executed when the user chose to scrape the site
    meaning if he want to get the search results by specifying
    song and artist.

    :return:
    """
    if scraper_obj.get_song() is None:
        print_status(NO_SEARCH, ERROR_COLOR)
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
        chosen_song = int(chosen_song) - 1
        scraper_obj.set_final_url(chosen_song)
        scraper_obj.update_song(scraper_obj.search_results[chosen_song]['song_name'])
    scraper_obj.get_info()
    final_chords = scraper_obj.get_chords()
    chords_obj = chords.Chords(final_chords)
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
    parser = argparse.ArgumentParser(description=LONG_DESCRIPTION)
    parser.add_argument('search', help="Search for a song")
    parser.add_argument('-u', '--url', help="Specific url to scrape from")
    parser.add_argument('-c', '--complex', help="Complex mode. Adding search suggestions", action="store_true")
    parser.add_argument('--dont-delete', help="Don't delete the tmp (HTML FILE) file when the script is ended.", action="store_true")
    args = parser.parse_args()

    try:
        if args.complex:
            search = search.Search()
            song = complex(search, args.search)
        scrap = scraper.Scraper(args.search, args.url)
        if scrape(scrap) is False:
            sys.exit(0)
        open_command()
        if not args.dont_delete:
            import time
            time.sleep(1)
            os.remove(TMP)
    except KeyboardInterrupt:
        print("\nBye")
