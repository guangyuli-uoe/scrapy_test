import time

import scrapy


class AbcSpider(scrapy.Spider):

    song_n = 0
    name = 'abc'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.lyrics.com/artists/G/80']

    # 生成通用对url
    url = 'https://www.lyrics.com/artists/G/%d'
    page_num = 82
    '''
        https://www.lyrics.com/artist        /A-%26-D/2137936791
    '''
    def parse(self, response):
        test1 = response.xpath('//*[@id="content-body"]/div/div[2]/table/tbody/tr')

        for tr in test1:
            # artist = tr.xpath('./td[1]/a/text()').extract()
            # artist = tr.xpath('./td[1]/a/text() | ./td[1]/strong/a/text()').extract()
            # print(artist)
            artist_url = ''.join(tr.xpath('./td[1]/a/@href | ./td[1]/strong/a/@href').extract())
            # print(artist_url)
            base_url = 'https://www.lyrics.com/artist/{}'.format(artist_url)
            print(base_url)
            yield scrapy.Request(url=base_url, callback=self.parse_artist)



        if self.page_num <= 90:

            new_url = format(self.url%self.page_num)
            self.page_num += 1

            yield scrapy.Request(url=new_url, callback=self.parse)


    '''
        https://www.lyrics.com    /lyric-lf/4846253/A+%26+D/Rugburn
        
        /lyric-lf/4846253/A+%26+D/Rugburn
    '''
    def parse_artist(self, response):

        tbody = response.xpath('//*[@id="content-body"]/div[3]/div/table/tbody/tr')

        for tr in tbody:
            song_url = ''.join(tr.xpath('./td[1]/strong/a/@href').extract())
            # print(song_url)
            base_url = 'https://www.lyrics.com/{}'.format(song_url)
            # yield scrapy.Request(url=base_url, callback=self.parse_song)
            # print(base_url)
            # song_url = tr.xpath('./td[1]/strong/a/@href').extract()
            # print(song_url)

            yield scrapy.Request(url=base_url, callback=self.parse_song)

    def parse_song(self, response):
        self.song_n += 1

        song_name = ''.join(response.xpath('//hgroup/h1/text()').extract())
        # print(song_name)
        artist_name = ''.join(response.xpath('//hgroup/h3/a/text()').extract_first())
        # print(artist_name)
        duration = ''.join(response.xpath('//div[@class="lyric-details"]/dl/dd[1]/text()').extract())
        # print(duration)

        lyrics = ''
        aaa = response.xpath('//div[@class="lyric clearfix"]/pre')
        aaa = aaa.xpath('string(.)').extract()
        aaa = ''.join(aaa)
        # print(aaa)

        yield {
            'N': self.song_n,
            'page': self.page_num,
            'title': song_name,
            'artist': artist_name,
            'duration': duration,
            'lyrics': aaa
        }







