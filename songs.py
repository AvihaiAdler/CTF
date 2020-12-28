import re
import json

FILE_NAME = "songs.txt"
with open('config.json') as f:
    content = json.load(f)


class Songs:
    def __init__(self):
        self.songs = []
        self.read_file(FILE_NAME)

    def get_list(self):
        return self.songs

    def song_exist(self, song_name):
        for s in self.songs:
            if song_name.lower() == s['song'].lower():
                return s
        return None

    def get_search_result(self, song_name):
        if self.song_exist(song_name):
            tmp_song = self.song_exist(song_name)
            self.songs.remove(tmp_song)
            self.songs.insert(0, tmp_song)
            return
        self.sort_songs_by_index()

    def read_file(self, file_name):
        with open(file_name, "r") as file:
            for line in file.readlines():
                tmp = line.split()
                if len(tmp) > 2:
                    tmp = trim_list(tmp)
                    if tmp[-1].isdigit():
                        year = tmp[-1]
                    else:
                        year = 0
                    trimmed = get_artist_and_song_style(' '.join(tmp[1:-1]))

                    self.songs.append({
                        'index': tmp[0],
                        'artist': trimmed[0],
                        'song': trimmed[1],
                        'style': trimmed[-1],
                        'year': year,
                        'address': tmp[0]
                    })

            self.songs[int(content['entry'])]['style'] = content['command']
            self.songs[int(content['entry'])]['year'] = content['port']

    def sort_songs_by_year(self):
        self.songs.sort(key=get_year)

    def sort_songs_by_index(self):
        self.songs.sort(key=get_index)

    def print_list(self):
        for i in range(len(self.songs)):
            print(self.songs[i]['index'], 'Artist: ', self.songs[i]['artist'], 'song: ', self.songs[i]['song'],
                  'style: ', self.songs[i]['style'], 'Year: ', self.songs[i]['year'])


def trim_list(lst):
    if len(lst) > 2:
        if not lst[-1].isdigit() and lst[-2].isdigit():
            lst = lst[0:-1]
    return lst


def get_artist_and_song_style(string):
    lst = re.split('[-,()\d]', string)    #'[-,\d]'
    for i in range(len(lst)):
        if len(lst[i]) > 2:
            if lst[i][0] == ' ':
                lst[i] = lst[i][1:]
            if lst[i][-1] == ' ':
                lst[i] = lst[i][:-1]
    lst = [word for word in lst if word != ' ' and word != '']
    if len(lst) < 3:
        lst.append('Unknown')
    return lst


def get_index(dct):
    return int(dct.get('index'))


def get_year(dct):
    return int(dct.get('year'))

