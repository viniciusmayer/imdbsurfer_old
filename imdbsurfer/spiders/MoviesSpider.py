import scrapy

from imdbsurfer import items

def votes(value):
    return cls(value, 1)

def index(value):
    return cls(value).replace('.', '')

def year(value):
    return cls(value).replace('(', '').replace(')', '')

def minutes(value):
    return value[0].split()[0].rstrip().lstrip().strip('\n').strip('\t').strip('\r')

def genres(value):
    _value = []
    for i in value[0].split(","):
        _value.append(i.rstrip().lstrip().strip('\n').strip('\t').strip('\r'))
    return _value

def link(value):
    _value = value[0]
    return _value[:_value.find('?') - 1]

def cls(value, pos=0):
    if len(value) > 0:
        return value[pos].rstrip().lstrip().strip('\n').strip('\t').strip('\r')
    else:
        return None
    

class MoviesSpider(scrapy.Spider):
    name = "movies"
    start_urls = [
        'http://www.imdb.com/search/title?count=100&genres=adventure,biography&num_votes=10000,&title_type=feature&sort=user_rating,desc',
    ]

    def parse(self, response):
        for i in response.css('div[class="lister-item-content"]'):
            item = items.Movie()
            item['index'] = index(i.css('h3[class="lister-item-header"]').css('span[class="lister-item-index unbold text-primary"]::text').extract())
            item['year'] = year(i.css('h3[class="lister-item-header"]').css('span[class="lister-item-year text-muted unbold"]::text').extract())
            item['link'] = link(i.css('h3[class="lister-item-header"]').css('a::attr(href)').extract())
            item['name'] = cls(i.css('h3[class="lister-item-header"]').css('a::text').extract())
            item['genres'] = genres(i.css('p[class="text-muted "]').css('span[class="genre"]::text').extract())
            item['minutes'] = minutes(i.css('p[class="text-muted "]').css('span[class="runtime"]::text').extract())
            item['rate'] = cls(i.css('div[class="ratings-bar"]').css('div[class="inline-block ratings-imdb-rating"]').css('strong::text').extract())
            item['metascore'] = cls(i.css('div[class="ratings-bar"]').css('div[class="inline-block ratings-metascore"]').css('span[class="metascore  favorable"]::text').extract())
            item['director'] = cls(i.css('p[class=""]').css('a::text').extract())
            item['votes'] = votes(i.css('p[class="sort-num_votes-visible"]').css('span::text').extract())            
            yield item