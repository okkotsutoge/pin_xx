import re
import urllib
from DrissionPage import ChromiumPage
from lxml import etree
from DownloadKit import DownloadKit


class PinterestImageSet():
    # 初始化
    def __init__(self):
        pass

    def search(self, key, slide=0, random=False):
        self.keyword={"q": key}
        key=urllib.parse.urlencode(self.keyword)
        self.url= f"https://www.pinterest.com/search/pins?{key}" if not random else "https://www.pinterest.com/"

        page=ChromiumPage()
        page.get(self.url)
        page.wait.load_start()

        for single_slide in range(slide):
            page.wait.load_start()
            print(f'正在翻至第{single_slide+1}页，请不要关闭页面...')
            page.scroll.to_bottom()

        self.content=page.html
        html = etree.HTML(self.content, etree.HTMLParser())

        page.close()

        try:
            img_gallery = html.xpath("//img/@srcset")
            img_gallery = [img.split(',')[-1].replace('4x', '').strip() for img in img_gallery] if img_gallery else []

            img_set = html.xpath("//link/@imagesrcset")
            img_set = [img.split(',')[-1].replace('4x', '').strip() for img in img_set] if img_set else []

            thumb_imgs = html.xpath('//*[@data-test-id="pinRepPresentation"]//img/@src')
            remv_sub = re.compile('\/[0-9]{3}x\/')
            thumb_imgs = [remv_sub.sub(r'/originals/', img) for img in thumb_imgs] if thumb_imgs else []

            text = re.findall(r'<script id="__PWS_DATA__" type="application\/json">' + '(.*)' + '</script>',
                              self.content)
            added_lists = re.findall(r'\"orig\":(.*?)}}', text[0])
            added_lists = [re.findall(r'\"url\":\"(.*?)\"', item)[0] for item in added_lists] if added_lists else []
        except Exception as e:
            pass

        images = added_lists+ thumb_imgs + img_gallery + img_set
        self.images= list(set([img for img in images if "originals" in img]))

    def downloadAll(self, targetUrl='./'):
        print('开始下载......')
        d = DownloadKit()
        d.set.goal_path(targetUrl)
        for img in self.images:
            d.add(img)
        d.wait()
        print('下载完毕!')


if __name__ == '__main__':
    pin = PinterestImageSet()
    key="sky"
    pin.search(key,random=True, slide=6)
    pin.downloadAll('C://{}'.format(key))
