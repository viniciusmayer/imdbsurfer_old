import scrapy
import itertools

from imdbsurfer import items

def artists(a, b):
    _a = []
    for i in a:
        _a.append(clean(i))
    _b = []
    for i in b:
        _b.append(clean(i))
    _b.remove('')
    return list(itertools.chain.from_iterable(zip(_b,_a)))

def directors(value):
    _value = value[1:value.index('Stars:')]
    return [v for v in _value if v != ',']

def stars(value):
    _value = value[value.index('Stars:') + 1:len(value)]
    return [v for v in _value if v != ',']

def genres(value):
    _value = []
    for i in value[0].split(","):
        _value.append(clean(i))
    return _value

def clean(value):
    if value is not None:
        return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
    return None

class MoviesSpider(scrapy.Spider):
    genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'film_noir', 'game_show', 'history',
              'horror', 'music', 'musical', 'mystery', 'news', 'reality_tv', 'romance', 'sci_fi', 'sport', 'talk_show', 'thriller', 'war', 'western']
    name = "movies"
    start_urls = []
    for i in genres:
        url = 'http://www.imdb.com/search/title?genres={0}&num_votes=10000,&title_type=feature&sort=user_rating,desc' 
        start_urls.append(url.format(i)) 

    def parse(self, response):
        for i in response.css('div[class="lister-item mode-advanced"]'):
            item = items.Movie()
            item['index'] = i.css('div[class="lister-item-content"]').css('h3[class="lister-item-header"]').css('span[class="lister-item-index unbold text-primary"]::text').extract()
            item['year'] = i.css('div[class="lister-item-content"]').css('h3[class="lister-item-header"]').css('span[class="lister-item-year text-muted unbold"]::text').extract()
            item['link'] = i.css('div[class="lister-item-content"]').css('h3[class="lister-item-header"]').css('a::attr(href)').extract()
            item['name'] = i.css('div[class="lister-item-content"]').css('h3[class="lister-item-header"]').css('a::text').extract()
            item['genres'] = genres(i.css('div[class="lister-item-content"]').css('p[class="text-muted "]').css('span[class="genre"]::text').extract())
            item['minutes'] = i.css('div[class="lister-item-content"]').css('p[class="text-muted "]').css('span[class="runtime"]::text').extract()
            item['rate'] = i.css('div[class="lister-item-content"]').css('div[class="ratings-bar"]').css('div[class="inline-block ratings-imdb-rating"]').css('strong::text').extract()
            item['metascore'] = i.css('div[class="lister-item-content"]').css('div[class="ratings-bar"]').css('div[class="inline-block ratings-metascore"]').css('span[class="metascore  favorable"]::text').extract()
            a = i.css('div[class="lister-item-content"]').css('p[class=""]').css('a::text').extract()
            b = i.css('div[class="lister-item-content"]').css('p[class=""]::text').extract()
            c = artists(a, b)
            item['directors'] = directors(c)
            item['stars'] = stars(c)
            item['votes'] = i.css('div[class="lister-item-content"]').css('p[class="sort-num_votes-visible"]').css('span::text').extract()
            yield item