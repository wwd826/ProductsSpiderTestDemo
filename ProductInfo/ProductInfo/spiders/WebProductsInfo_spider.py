# -*- coding: utf-8 -*-
import scrapy
from ProductInfo.items import ProductinfoItem
#跳转界面循环解析商品内容
class WebproductsinfoSpiderSpider(scrapy.Spider):
    #爬虫名称
    name = 'WebProductsInfo_spider'
    #允许的域名
    allowed_domains = ['www.eastbay.com']
    #入口的url，传参到调度器中
    start_urls = ['https://www.eastbay.com/_-_/keyword-mens+adidas+harden+shoes']

    def parse(self, response):
        #print (response.text)
        #获取商品列表
        productList =response.xpath("//div[@class='mainsite_record_listing']//div[@id='endeca_search_results']//ul/li[@data-sku]")
        for product_item in productList:
            #print(product_item)
            product_info = ProductinfoItem()
            #获取title
            product_info["title"] = product_item.xpath(".//span[@class='product_title']/text()").extract_first()
            #获取价格（售价）
            product_info["price"] = product_item.xpath(".//span//span[@class='price']/text()").extract_first()
            #颜色
            product_info["color"] ="".join(product_item.xpath(".//span[@class='other_product_attributes']//span[@class='color']/text()").extract_first().split())
            #尺码
            product_info["size"]="".join(product_item.xpath(".//span[@class='other_product_attributes']//span[@class='width']/text()").extract_first().split())
            #简介
            product_info["details"]="".join(product_item.xpath("//span[@class='other_product_attributes']//span[@class='short_description']/text()").extract_first().split())
            #网站的编号
            product_info["sku"]=product_item.xpath("./@data-sku").extract_first()
            #大图的url
            product_info["img_urls"]=product_item.xpath(".//a[1]//span[@class='product_image']//img/@data-original").extract()
            print(product_info)
            yield  product_info
        #跳转页面 通过回调函数进行爬取 其他界面
        #但是本界面跳转不是插件的方式，是静态写死的  故采取该方法
        for list_page in ["2","3"]:
            page_href ="//div[@class='searchResultsPaging topPaging']//div[@class='itemsPerPage']//ul//li["+list_page+"]/a/@href"
            next_link = response.xpath(page_href).extract()
            if next_link:
                next_link=next_link[0]
                yield scrapy.Request("https://www.eastbay.com"+next_link,callback=self.parse)

