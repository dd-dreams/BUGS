# BUGS - Better Ultimate Guitar Scraper
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dd-dreams/BUGS) ![GitHub](https://img.shields.io/github/license/dd-dreams/BUGS) ![Python-Version](https://img.shields.io/badge/Python-3.7-blue.svg)
***
This is a scraper/unofficial-API for [Ultimate-Guitar.](https://ultimate-guitar.com) It can scrape for you the chords, and output them in a nice HTML format. 
Fast, easy and very lightweight.

***
# Features
* Autoscroll
* Centered chords
* Fast
* Bolded chords
* Random headers/user-agent

***
# Usage
`$ python cli.py -h`:
```
usage: cli.py [-h] [-u URL] [-c] [--dont-delete] search

Scrape Ultimate Guitar website with no tracking, fast, easy, and lightweight. You can
parse arguments and get instant results. Enjoy!

positional arguments:
  search             Search for a song

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Specific url to scrape from
  -c, --complex      Complex mode. Adding search suggestions
  --dont-delete      Don't delete the tmp (HTML FILE) file when the script is ended
```
You specify a search query, and the script will get for you the list of songs that
the script had found. Next you choose the final song, and it will output to a temporary HTML file
and open that file for you. Easy as that.

`--complex`: Optional search tool. Using the search bar in the ultimate-guitar site, and gives you suggestions, until you choose the final keywords.
`--dont-delete`: As it had been said before, the script is creating a temporary HTML file to view the final chords, and then being deleted after the file had been opened.
If you want, you can choose to not delete the temporary HTML file, but it will be deleted when the next search happens.
***
# Examples
### Example 1
```
$ python cli.py "perfect ed sheeran"
[*] Fetching results                                             
[*] Successfully scraped
[*] Songs have been found. Showing results...
    [1] Artist: Ed Sheeran, Perfect, Rating: 37199, Chords
    ...
    ...
Choose song (Enter for next page):
```
### Example 2
```
$ python cli.py -c "per"
[*] [1] perfect
[*] [2] perfect ed sheran
[*] [3] ...
Search (Enter for search results): perfe
[*] [1] perfect
[*] [2] perfect ed sheran
[*] [3] ...
Search (Enter for search results): 1
[*] Fetching results
[*] Successfully scraped
[*] Songs have been found. Showing results...
    [1] Artist: Ed Sheeran, Perfect, Rating: 37199, Chords
    ...
    ...
Choose song (Enter for next page):
```
***
# LICENSE
MIT license.