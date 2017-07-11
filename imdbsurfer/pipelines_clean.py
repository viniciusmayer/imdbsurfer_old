# -*- coding: utf-8 -*-
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import itertools, re

class CleanPipeline(object):
    def process_item(self, item, spider):
        item['index'] = self.cleanInteger(item['index'][0])
        item['votes'] = self.cleanInteger(item['votes'][1])
        item['minutes'] = self.cleanInteger(item['minutes'][0]) if len(item['minutes']) > 0 else None
        item['metascore'] = self.cleanInteger(item['metascore'][0]) if len(item['metascore']) > 0 else None
        
        item['name'] = self.cleanString(item['name'][0])
        item['rate'] = self.cleanString(item['rate'][0])

        item['year'] = self.getYear(item['year'][0])
        item['link'] = self.getLink(item['link'][0])
        item['genres'] = self.getGenres(item['genres'][0])
        c = self.getArtists(item['artistsa'], item['artistsb'])
        item['directors'] = self.getDirectors(c)
        item['stars'] = self.getStars(c)
        item['genre'] = self.getGenre(item['url'])
        item['type'] = self.getType(item['url'])
        return item

    def getYear(self, value):
        begin = re.search("\d", value).start()
        return value[begin:begin+4]

    def getGenre(self, value):
        return value[value.find('genres') + 7:value.find('num_votes') - 1]

    def getType(self, value):
        return value[value.find('title_type') + 11:value.find('sort') - 1] 

    def getArtists(self, a, b):
        _a = []
        for i in a:
            _a.append(self.cleanString(i))
        _b = []
        for i in b:
            _b.append(self.cleanString(i))
        _b.remove('')
        return list(itertools.chain.from_iterable(zip(_b, _a)))
    
    def getDirectors(self, value):
        end = None
        try:
            end = value.index('Stars:') 
        except ValueError:
            pass
        if (end is None):
            try:
                end = value.index('Star:')
            except ValueError:
                pass
        _value = value[1:end]
        return [v for v in _value if v != ',']
    
    def getStars(self, value):
        begin = None
        try:
            begin = value.index('Stars:') 
        except ValueError:
            pass
        if (begin is None):
            try:
                begin = value.index('Star:')
            except ValueError:
                pass
        if (begin is None):
            return None
        _value = value[begin + 1:len(value)]
        return [v for v in _value if v != ',']

    def getGenres(self, value):
        _value = []
        for i in value.split(","):
            _value.append(self.cleanString(i))
        return _value

    def getLink(self, value):
        return 'http://www.imdb.com{0}'.format(value[:value.find('?') - 1])

    def cleanInteger(self, value):
        return ''.join(i for i in value if i.isdigit())
    
    def cleanString(self, value):
        if (value is not None):
            return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
        return None
