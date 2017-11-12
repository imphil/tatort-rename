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

# Show ID of the Tatort series on tvdb.com
TVDB_TATORT_SHOW_ID = 83214

def search_episode_by_filename(filename):
    # Split out file extension
    basename, extension = os.path.splitext(filename)

    # Remove common phrases not part of the title
    searchname = re.sub(r"Tatort", '', basename)

    # Find match
    match_results = process.extractBests(searchname, tatort_titles,
                                         score_cutoff = 60, limit = 5)

    # no match was found
    if not match_results:
        print("No match was found for file {}".format(filename))
        return

    # only one match was found with the minimum required score
    matching_episode = None
    if len(match_results) == 1:
        chosen_result = match_results[0]

    # multiple matches were found above the score threshold: ask the user
    # which one is right
    if len(match_results) > 1:
        if match_results[0][1] - match_results[1][1] > 20:
            # if choice 0 is 20 points more likely than choice 1, we directly
            # use the first choice
            chosen_result = match_results[0]
        else:
            # print choices
            print("Multiple matches were found for file {}".format(filename))
            print("Please choose the correct one from the list below.")
            for index, match_result in enumerate(match_results):
                (matching_title, matching_score, matching_id) = match_result
                episode = tatort_episodes[matching_id]
                print("{index}: {name} (score: {score:02d}/100)".format(
                    index = index, name = episode['episodename'],
                    score = matching_score))

            # let user choose
            chosen_id = int(input('Your choice: '))
            # FIXME: repeat on wrong inputs

            chosen_result = match_results[chosen_id]

    (matching_title, matching_score, matching_id) = chosen_result
    matching_episode = tatort_episodes[matching_id]

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
    show = t[TVDB_TATORT_SHOW_ID]

    # Build a dict of all show titles, indexed by the TVDB episode ID
    # Note: we need to use dicts here and not lists, as fuzzywuzzy only returns
    # the matching ID when using a dict, not a list.
    tatort_episodes = {}
    tatort_titles = {}
    for cur_season in show.values():
        for cur_episode in cur_season.values():
            episode_id = cur_episode['id']

            # Prepare the title string used for matching the filename
            # We filter the title as we get it from TVDB to contain only the
            # title. Example:
            # "Episode 2016x39 - Janneke & Brix - 05 - Land in dieser Zeit"
            # becomes
            # "Land in dieser Zeit".
            episode_title = re.sub(r"^(.+) - (.+) - (.+)$", "\\3",
                                   cur_episode['episodename'])

            tatort_episodes[episode_id] = cur_episode
            tatort_titles[episode_id] = episode_title

    main()
