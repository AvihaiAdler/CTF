import re
import json

songs_file = 'ctf/data/songs.txt'
config_file = 'ctf/data/config.json'

with open(config_file) as conf:
    content = json.load(conf)


class Secrets:
    def __init__(self):
        self.username = content['username']
        self.password = content['password']
        self.search_string = content['search_string']
        self.flag = content['flag']
        self.cookie_value = content['cookie']
        self.default_cookie = 'vanilla'


class Songs:
    def __init__(self):
        self.songs = []
        self.read_file(songs_file)

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

            self.songs[int(content['entry'])]['style'] = 'cookie:'
            self.songs[int(content['entry'])]['year'] = content['cookie']

    def sort_songs_by_index(self):
        self.songs.sort(key=get_index)

    def get_index_by_name(self, song_name):
        for song in self.songs:
            if song['song'].lower() == song_name.lower():
                return song['index']
        return "#"


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


