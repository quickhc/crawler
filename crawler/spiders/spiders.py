import scrapy

from crawler.items import CrawlerItem


class DemoSpider(scrapy.spiders.Spider):
    name = "crawler"
    allowed_domains = ["jianshu.com"]
    # 设置URL
    url = 'https://www.jianshu.com/'
    # 记录当前访问下标
    index = 0
    # 默认url
    start_urls = [url]

    def parse(self, response):
        print("----------------------------------------------------------------------------")

        # xpath匹配规则
        for each in response.xpath("//li"):
            item = CrawlerItem()
            try:
                item["title"] = each.xpath("./div/a/text()").extract()[0]
            except:
                item["title"] = '空'

            try:
                item["name"] = each.xpath("./div/div[1]/div/a/text()").extract()[0]
            except:
                item["name"] = '空'

            try:
                item["href"] = 'https://www.jianshu.com' + each.xpath("./div/div[2]/a[2]/@href").extract()[0]
            except:
                item["href"] = '空'

            try:
                item["type"] = each.xpath("./div/div[2]/a[1]/text()").extract()[0]
            except:
                item["type"] = '空'

            try:
                item["time"] = each.xpath("./div/div[1]/div/span/@data-shared-at").extract()[0]
            except:
                item["time"] = '空'

            try:
                extract = 'https://www.jianshu.com' + each.xpath("./div/div[2]/a[1]/@href").extract()[0]
                if (DemoSpider.start_urls.count(extract) == 0):
                    DemoSpider.start_urls.insert(DemoSpider.start_urls.__len__(), extract)
                else:
                    pass
            except:
                pass
            # 把数据交给管道文件
            yield item

        DemoSpider.index = DemoSpider.index + 1
        if (DemoSpider.index < DemoSpider.start_urls.__len__() - 1):
            # 把请求交给控制器
            yield scrapy.Request(self.url[DemoSpider.index], callback=self.parse)
        else:
            pass

# class DemoSpider(scrapy.spiders.Spider):
#     name = "crawler"
#     allowed_domains = ["tencent.com"]
#     # 设置URL
#     url = 'http://hr.tencent.com/position.php?&start='
#     # 设置页码
#     offset = 0
#     # 默认url
#     start_urls = [url + str(offset)]
#
#     def parse(self, response):
#         print("----------------------------------------------------------------------------")
#
#         # xpath匹配规则
#         for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
#             item = CrawlerItem()
#             # 职位名
#             item["positionname"] = each.xpath("./td[1]/a/text()").extract()[0]
#             # 详细链接
#             item["positionLink"] = each.xpath("./td[1]/a/@href").extract()[0]
#             # 职位类别
#             try:
#                 item["positionType"] = each.xpath("./td[2]/text()").extract()[0]
#             except:
#                 item["positionType"] = '空'
#             # 招聘人数
#             item["peopleNum"] = each.xpath("./td[3]/text()").extract()[0]
#             # 工作地点
#             item["workLocation"] = each.xpath("./td[4]/text()").extract()[0]
#             # 发布时间
#             item["publishTime"] = each.xpath("./td[5]/text()").extract()[0]
#             # 把数据交给管道文件
#             yield item
#         # 设置新URL页码
#         if (self.offset < 1):
#             self.offset += 10
#         # 把请求交给控制器
#         yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
