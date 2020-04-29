import requests
import re
from lxml import etree
from fontTools.ttLib import TTFont
from woff2otf import convert
from fontOCR import font_convert


class CrawlCat:
    def __init__(self):
        self.cookie = '__mta=188702359.1587907186008.1588140234659.1588140424133.16; uuid_n_v=v1; uuid=96CC667087C011EAB9C1D52EE5BDD7B9ED377F1627A94203966C12246722351E; mojo-uuid=b5d5bab2be9cfdb9b2226b6f025c748f; _lxsdk_cuid=171b6a4cd18c8-08b5dd064c46b-7373667-1fa400-171b6a4cd19c8; _lxsdk=96CC667087C011EAB9C1D52EE5BDD7B9ED377F1627A94203966C12246722351E; t_lxid=171b6a4cd6cc8-0526c209fbca32-7373667-1fa400-171b6a4cd6cc8-tid; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1587994186,1588000721,1588133459,1588137298; mojo-session-id={"id":"f8250f61b70b3a3211a7c8385323441f","time":1588140234624}; __mta=188702359.1587907186008.1588133480646.1588140281584.6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1588140424; mojo-trace-id=3; _lxsdk_s=171c488d3c0-ec-85e-8fa%7C%7C5'
        self.base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        'cookie':self.cookie
    }

    def getHtml(self,url, options={}):
        headers = dict(self.base_headers, **options)
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print("状态码不对")
        else:
            res.encoding = 'utf-8'
            return res

    def downWoff(self,url,filePath='font.woff'):    ##下载woff文件
        res = self.getHtml(url)
        with open(filePath, 'wb') as f:
            f.write(res.content)

    def crawl(self):
        url = "https://maoyan.com/films/1277939"
        res = self.getHtml(url).text
        onlineWoff = re.findall(r"url\('(//vfile\.meituan\.net.*?\.woff)'\)", res)[0]
        self.downWoff('https:'+onlineWoff)   #下载woff文件
        convert('font.woff','font.otf')      #字体转换
        maping = font_convert('font.otf')    #code映射对应表
        for k,v in maping.items():           #替换
            res = str(res).replace(k,v)
        html = etree.HTML(res)
        score = html.xpath("//span[@class='index-left info-num ']/span/text()")[0]
        boxOffice = html.xpath("//div[@class='movie-index-content box']/span/text()")[0]

        print(score,boxOffice)

if __name__ == '__main__':
    c = CrawlCat()
    c.crawl()

