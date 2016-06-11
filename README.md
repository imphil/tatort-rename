# Rename files of Tatort episodes (the German TV series) in an uniform way

In many cases, the files have been downloaded from different sites and are
named in various ways. This script uses fuzzy matching together with a
database of all Tatort titles to determine the most likely episode. The file
is then renamed following a common convention.

A common way to download Tatort episodes is using
[Mediathekview](http://zdfmediathk.sourceforge.net/) or recording them from
a DVB source. Those files are handled well.

```shell
$> tatort-rename.py
Tatort-Das_Recht,_sich_zu_sorgen-1004093911.mp4 -> Tatort 0988 - 2016x20 - Voss - 02 - Das Recht, sich zu sorgen.mp4
Tatort-Ein_Fuß_kommt_selten_allein-1024059245.mp4 -> Tatort 0986 - 2016x18 - Thiel - 29 - Ein Fuß kommt selten allein.mp4
Tatort-Wir_-_Ihr_-_Sie-0253336963.mp4 -> Tatort 0989 - 2016x21 - Karow - 03 - Wir-Ihr-Sie.mp4
Tatort-Der_hundertste_Affe-0492381611.mp4 -> Tatort 0987 - 2016x19 - Lürsen & Stedefreund - 33 - Der hundertste Affe.mp4
Tatort-Zirkuskind-0794861723.mp4 -> Tatort 0900 - 2014x08 - Odenthal - 59 - Zirkuskind.mp4
```

## Usage
Change to the folder containing your movie files and run `tatort-rename.py`.

```shell
cd your_movie_file_folder
./tatort-rename.py
```

## Installation

### Requirements
- Python 3
- [tvdb_api](https://github.com/dbr/tvdb_api)
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)

### Install Modules
```shell
sudo pip install fuzzywuzzy
sudo easy_install tvdb_api
```

## Author
Philipp Wagner <mail@philipp-wagner.com>

## License
This script is MIT licensed.
