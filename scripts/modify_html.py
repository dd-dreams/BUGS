#!/usr/bin/python3

from constants.html_addons import *


def add_basic(file, start_or_end):
    """
    function for adding the default html tags like: <html> and so on

    :param file: file object
    :param start_or_end: add basic html to start of the file or the end of the file

    """
    if start_or_end:
        file.write(HTML_BASICS_START)
    else:
        file.write(HTML_BASICS_END)


def center_smooth_html(file, start_or_end):
    """
    function for centering the text and adding smooth scroll

    """
    if start_or_end:
        file.write(CENTER_SMOOTH_TEXT_START)
    else:
        file.write(CENTER_TEXT_END)


def add_button(file):
    file.write(AUTO_SCROLL_BUTTON)


def add_autoscroll(file):
    file.write(AUTO_SCROLL_SCRIPT)
