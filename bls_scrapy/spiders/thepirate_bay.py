import scrapy
from scrapy import Selector as S
from scrapy.http import Request as R
from bls_scrapy.items import BlsScrapyItem


class ThepirateBaySpider(scrapy.Spider):
    name = "thepirate_bay"
    item = BlsScrapyItem()
    allowed_domains = ['thepirate-bay.org', 'www.pirate-bay.net', 'tpb.party']
    start_urls = ['https://tpb.party/browse','https://tpb.party/top']
    agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.777 (beta) Yowser/2.5 Safari/537.36'

    def start_requests(self):
        requests = []
        for url in self.start_urls:
            requests.append(R(url=url, headers={'User-Agent': self.agent}))

        return requests

    @staticmethod
    def _get_size(string):
        import re
        match = re.search(r'Size\s(\d*.?\d*)\s(\w*)', string)
        if match is None: return 0
        size = float(match.group(1))
        dim = match.group(2)
        return {
            dim == 'KiB': size / 1024,
            dim == 'MiB': size,
            dim == 'GiB': size * 1024,
        }[True]

    @staticmethod
    def _get_released(string):
        import re
        import datetime
        released = datetime.datetime.now()
        match = re.search(r'Uploaded\s((.*)\s(\d*:\d*)|(\d*)\smins?\sago|((.*)\s\d*))\,\sSize', string)

        if match is None: return released.timestamp()

        if match.group(2) is not None and match.group(2) == 'Y-day':
            released = released - datetime.timedelta(days=1)
            released = released.replace(hour=int(match.group(3).split(':')[0]),
                                        minute=int(match.group(3).split(':')[1]))
        elif match.group(2) is not None and match.group(2) == 'Today':
            released = released.replace(hour=int(match.group(3).split(':')[0]),
                                        minute=int(match.group(3).split(':')[1]))
        elif match.group(4) is not None:
            released = released - datetime.timedelta(minutes=int(match.group(4)))
        else:
            dayMonthYear = re.split(r'\s', match.group(1))
            dayMonth = dayMonthYear[0]
            released = released.replace(month=int(dayMonth.split('-')[0]),
                                        day=int(dayMonth.split('-')[1]))
            if ':' in dayMonthYear[1]:
                released = released.replace(hour=int(dayMonthYear[1].split(':')[0]),
                                            minute=int(dayMonthYear[1].split(':')[1]))
            else:
                released = released.replace(year=int(dayMonthYear[1]))

        return released.timestamp()

    def parse(self, response):
        for row in response.xpath("//table/tr/td[@class='categoriesContainer']/dl/dt").getall():
            category_url = S(text=row).xpath('//a/@href').get()
            is_top = ('top' == category_url.rsplit("/")[-2])
            if not is_top:
                category_url += '/1/7/0'
            if category_url is not None:
                yield response.follow(
                    url=category_url,
                    headers={'User-Agent': self.agent},
                    callback=self.parse_category,
                    meta={
                        'category': S(text=row).xpath('//a/text()').get(),
                    }
                )
                self.item['category'] = S(text=row).xpath('//a/text()').get()
                

    def parse_category(self, response):
        result = response.meta.copy()
        torrents = []
        for row in response.xpath('//div[@id="content"]/div[@id="main-content"]/table[@id="searchResult"]/tr').getall():
            url = S(text=row).xpath('//td/div[@class="detName"]/a/@href').get()
            if url is not None:
                torrent = {
                    'verified': S(text=row).xpath('//td/a[2]/@href').get() is not None,
                    'sub_category': S(text=row).xpath('//td[@class="vertTh"]/center/a[2]/text()').get(),
                    'url': url,
                    'title': S(text=row).xpath('//td/div[@class="detName"]/a/text()').get(),
                    'magnet': S(text=row).xpath('//td/a[@title="Download this torrent using magnet"]/@href').get(),
                    'seeds': S(text=row).xpath('//td[@align="right"][1]/text()').get(),
                    'peers': S(text=row).xpath('//td[@align="right"][2]/text()').get(),
                    'size': self._get_size(S(text=row).xpath('//font[@class="detDesc"]/text()').get()),
                    'released': self._get_released(S(text=row).xpath('//font[@class="detDesc"]/text()').get()),
                }        

                self.item['verified'] = torrent['verified']
                self.item['sub_category'] = torrent['sub_category']
                self.item['url'] = torrent['url']
                self.item['title'] = torrent['title']
                self.item['magnet'] = torrent['magnet']
                self.item['seeds'] = torrent['seeds']
                self.item['peers'] = torrent['peers']
                self.item['size'] = torrent['size']
                self.item['released'] = torrent['released']
                torrents.append(torrent)

        result.update({'torrents': torrents})
        yield result

    def parse_details(self, response):
        result = response.meta.copy()
        details = response.xpath('//div[@id="detailsframe"]/div[@id="details"]').get()
        result.update({
        })
        yield result