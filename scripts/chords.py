import os
from constants.other import CACHED_SITES, TMP
import modify_html


class Chords:
    def __init__(self, chords):
        """
        Constructor

        :param name: name of the file
        :param chords: chords to output
        """
        self.chords_class = "chords"
        self.name = TMP
        self.chords = chords

    @staticmethod
    def add_basic_html(file, start_or_end):
        """
        function for adding some basic html tags to outputted html file

        :param file: file object
        :param start_or_end: do we want to add the starting tags or ending ones
        :return: None
        """
        if start_or_end:
            modify_html.add_basic(file, start_or_end)
            modify_html.center_smooth_html(file, start_or_end)
        else:
            modify_html.center_smooth_html(file, start_or_end)
            modify_html.add_basic(file, start_or_end)

    def output_chords(self):
        """
        main method for adding all the basic html and outputting them
        it opens the file 3 times, since that's the ONLY way i could find to
        make the lines do new lines (i had to put p tags to act as \n).
        also made the chords bold
        :return:
        """
        with open(self.name, "w+") as file:  # writing the chords
            file.write(self.chords)
        with open(self.name, "r") as file:  # reading the chords
            lines = file.readlines()
        with open(self.name, "w+") as chords_html:  # changing the html
            self.add_basic_html(chords_html, True)
            modify_html.add_button(chords_html)
            for line in lines:  # making chords bold, and removing [tab] tags or whatever are those
                line = line.replace("[ch]", "<b>").replace("[/ch]", "</b>")\
                    .replace("[tab]", "").replace("[/tab]", "")
                chords_html.write(line)
            modify_html.add_autoscroll(chords_html)
            self.add_basic_html(chords_html, False)
