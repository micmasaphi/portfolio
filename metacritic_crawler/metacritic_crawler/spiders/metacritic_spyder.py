import scrapy
from scrapy.crawler import CrawlerProcess
import string


# gets all ratings and review briefs from critics
class CriticSpider(scrapy.Spider):

    name = "critics"
    start_urls = ['http://www.metacritic.com/browse/albums/publication/score?num_items=100']

    def parse(self, response):
        for publication in response.css('div.wrap h3'):
                # follow links to publication pages
                for href in response.css('div.wrap h3 a::attr(href)'):
                    yield response.follow(href, self.parse_publication)

        # follow pagination links
        for href in response.css('span.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_publication(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        # find proper elements to extract
        for album in response.css('div.review_wrap'):
            album_description = album.css('div.review_body::text').extract_first()
            album_description = album_description.strip(' \t\n\r')
            yield {
                'album id': album.css('div.review_product a::attr(href)').extract_first(),
                'publication name': album.css('li.publication_title::text').extract_first(),
                'album name': album.css('div.review_product a::text').extract_first(),
                'album rating': album.css('li.brief_critscore span.metascore_w::text').extract_first(),
                'album description': album_description,
            }

        for href in response.css('span.next a::attr(href)'):
            yield response.follow(href, self.parse_publication)


# gets all ratings from users
class AlbumSpider(scrapy.Spider):

    name = "albums"

    lettering = list(string.ascii_lowercase)
    lettering.insert(0, '')
    start_urls = list()

    for l in lettering:
        start_urls.append('http://www.metacritic.com/browse/albums/artist/' + l + '?view=detailed')

    def parse(self, response):
        for album in response.css('div.product_wrap'):
            img_url = album.css('img::attr(src)').extract_first()
            img_url = img_url.replace("-53","-98")

            artist = album.css('span.product_artist::text').extract_first()
            artist = artist.replace(" - ", "")

            genres = album.css('li.stat.genre span.data::text').extract_first()
            if genres is not None:
                genres = genres.strip(' \t\n\r')
                genres = [elem.strip() for elem in genres.split(",")]
                if '...' in genres:
                    genres.remove('...')

            mc_rating = album.css('span.metascore_w::text').extract_first()
            if mc_rating is 'tbd':
                mc_rating = None

            usr_rating = album.css('li.stat.product_avguserscore span.data::text').extract_first()

            yield {
                'id': album.css('h3.product_title a::attr(href)').extract_first(),
                'name': album.css('h3.product_title a::text').extract_first(),
                'img': img_url,
                'artist': artist,
                'genre(s)': genres,
                'mc rating': mc_rating,
                'usr rating': usr_rating,
            }

        # follow pagination links
        for href in response.css('span.next a::attr(href)'):
            yield response.follow(href, self.parse)


#process = CrawlerProcess()
#process.crawl(CriticSpider)
#process.crawl(UserSpider)
#process.start()
