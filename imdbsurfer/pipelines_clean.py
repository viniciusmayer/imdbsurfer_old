# -*- coding: utf-8 -*-
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import itertools
import re


def get_year(value):
    begin = re.search("\d", value).start()
    return value[begin:begin + 4]


def get_genre(value):
    return value[value.find('genres') + 7:value.find('num_votes') - 1].lower()


def get_type(value):
    return value[value.find('title_type') + 11:value.find('sort') - 1].lower()


def get_directors(value):
    end = None
    try:
        end = value.index('Stars:')
    except ValueError:
        pass
    if end is None:
        try:
            end = value.index('Star:')
        except ValueError:
            pass
    _value = value[1:end]
    return [v for v in _value if v != ',']


def get_stars(value):
    begin = None
    try:
        begin = value.index('Stars:')
    except ValueError:
        pass
    if begin is None:
        try:
            begin = value.index('Star:')
        except ValueError:
            pass
    if begin is None:
        return None
    _value = value[begin + 1:len(value)]
    return [v for v in _value if v != ',']


def get_link(value):
    return 'http://www.imdb.com{0}'.format(value[:value.find('?')])


def clean_integer(value):
    return ''.join(i for i in value if i.isdigit())


def clean_string(value):
    if value is not None:
        return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
    return None


def get_artists(a, b):
    _a = []
    for i in a:
        _a.append(clean_string(i))
    _b = []
    for i in b:
        _b.append(clean_string(i))
    _b.remove('')
    return list(itertools.chain.from_iterable(zip(_b, _a)))


def get_genres(value):
    _value = []
    for i in value.split(','):
        _value.append(clean_string(i).lower())
    return _value


class CleanPipeline(object):
    def process_item(self, item, spider):
        item['index'] = clean_integer(item['index'][0])
        item['votes'] = clean_integer(item['votes'][1])
        item['minutes'] = clean_integer(item['minutes'][0]) if len(item['minutes']) > 0 else None
        item['metascore'] = clean_integer(item['metascore'][0]) if len(item['metascore']) > 0 else None
        item['name'] = clean_string(item['name'][0])
        item['rate'] = clean_string(item['rate'][0])
        item['year'] = get_year(item['year'][0])
        item['link'] = get_link(item['link'][0])
        item['genres'] = get_genres(item['genres'][0])
        c = get_artists(item['artistsa'], item['artistsb'])
        item['directors'] = get_directors(c)
        item['stars'] = get_stars(c)
        item['genre'] = get_genre(item['url'])
        item['type'] = get_type(item['url'])
        return item
