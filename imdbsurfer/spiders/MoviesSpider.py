import scrapy

from imdbsurfer import items

def votes(value):
    return extractAndClean(value, 1)

def index(value):
    return extractAndClean(value).replace('.', '')

def year(value):
    return extractAndClean(value).replace('(', '').replace(')', '')

def minutes(value):
    return clean(value[0].split()[0])

def genres(value):
    _value = []
    for i in value[0].split(","):
        _value.append(clean(i))
    return _value

def link(value):
    return value[0][:value[0].find('?') - 1]

def extractAndClean(value, pos=0):
    if value is not None and len(value) > 0:
        return clean(value[pos])
    return None

def clean(value):
    if value is not None:
        return value.rstrip().lstrip().strip('\n').strip('\t').strip('\r')
    return None

class MoviesSpider(scrapy.Spider):
    genres = ['action',
        'adventure',
        'animation',
        'biography',
        'comedy',
        'crime',
        'documentary',
        'drama',
        'family',
        'fantasy',
        'film_noir',
        'game_show',
        'history',
        'horror',
        'music',
        'musical',
        'mystery',
        'news',
        'reality_tv',
        'romance',
        'sci_fi',
        'sport',
        'talk_show',
        'thriller',
        'war',
        'western']
    
    name = "movies"
    start_urls = []
    
    for i in genres:
        url = 'http://www.imdb.com/search/title?genres={0}&num_votes=10000,&title_type=feature&sort=user_rating,desc' 
        start_urls.append(url.format(i)) 

    def parse(self, response):
        for i in response.css('div[class="lister-item-content"]'):
            item = items.Movie()
            item['index'] = index(i.css('h3[class="lister-item-header"]').css('span[class="lister-item-index unbold text-primary"]::text').extract())
            item['year'] = year(i.css('h3[class="lister-item-header"]').css('span[class="lister-item-year text-muted unbold"]::text').extract())
            item['link'] = link(i.css('h3[class="lister-item-header"]').css('a::attr(href)').extract())
            item['name'] = extractAndClean(i.css('h3[class="lister-item-header"]').css('a::text').extract())
            item['genres'] = genres(i.css('p[class="text-muted "]').css('span[class="genre"]::text').extract())
            item['minutes'] = minutes(i.css('p[class="text-muted "]').css('span[class="runtime"]::text').extract())
            item['rate'] = extractAndClean(i.css('div[class="ratings-bar"]').css('div[class="inline-block ratings-imdb-rating"]').css('strong::text').extract())
            item['metascore'] = extractAndClean(i.css('div[class="ratings-bar"]').css('div[class="inline-block ratings-metascore"]').css('span[class="metascore  favorable"]::text').extract())
            item['director'] = extractAndClean(i.css('p[class=""]').css('a::text').extract())
            item['votes'] = votes(i.css('p[class="sort-num_votes-visible"]').css('span::text').extract())            
            yield item