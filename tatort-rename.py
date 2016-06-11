#!/usr/bin/python3
#
# Rename files of Tatort episodes (the German TV series) in an uniform way
#
# In many cases, the files have been downloaded from different sites and are
# named in various ways. This script uses fuzzy matching together with a
# database of all Tatort titles to determine the most likely episode. The file
# is then renamed following a common convention.
#
# Author: Philipp Wagner <mail@philipp-wagner.com>
# License: MIT
#

import tvdb_api
from fuzzywuzzy import process
import os
import re

def search_episode_by_filename(filename):
    # Split out file extension
    basename, extension = os.path.splitext(filename)

    # Remove common phrases not part of the title
    searchname = re.sub(r"Tatort", '', basename)

    # Find match
    (matching_title, matching_probability) = process.extractOne(searchname,
                                                                tatort_titles)
    matching_episode = tatort_episodes[tatort_titles.index(matching_title)]

    # build new file name
    try:
        absolute_number = int(matching_episode['absolute_number'])
    except:
        absolute_number = 0

    new_filename = "Tatort {:04d} - {:02d}x{:02d} - {}{}".format(
        absolute_number, int(matching_episode['seasonnumber']),
        int(matching_episode['episodenumber']),
        matching_episode['episodename'], extension)

    new_filename = new_filename.replace('/', ' ')

    print("{} -> {}".format(filename, new_filename))
    os.rename(filename, new_filename)


def main():
    for fn in os.listdir('.'):
        if os.path.isfile(fn):
            search_episode_by_filename(fn)

if __name__ == "__main__":
    t = tvdb_api.Tvdb(language='de')
    show = t['Tatort']

    # Build an array of all show titles
    tatort_titles = []
    tatort_episodes = []
    for cur_season in show.values():
        for cur_episode in cur_season.values():
            episode_title = re.sub(r"^(.+) - (.+) - (.+)$", "\\3",
                                   cur_episode['episodename'])
            tatort_titles.append(episode_title)
            tatort_episodes.append(cur_episode)

    main()
