from scrapy import cmdline
#cmdline.execute('scrapy crawl WebProductsInfo_spider'.split())
#开启爬虫  并将爬取的内容放到保存到本地
cmdline.execute("scrapy crawl  WebProductsInfo_spider  -o productInfo.json".split())