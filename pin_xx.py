import os
import re
import urllib
import random
import requests
from DrissionPage import ChromiumPage
from lxml import etree
import time


class PinterestImageSet():
    # 初始化
    def __init__(self, headers=None):
        pass

    def search(self, key, slide=0):
        self.keyword={
            "q": key
        }
        self.url='https://www.pinterest.com/search/pins?{}'.format(urllib.parse.urlencode(self.keyword))

        page=ChromiumPage()
        page.get(self.url)
        page.wait.load_start()

        for single_slide in range(slide):
            print(f'正在翻至第{slide}页，请不要关闭页面...')
            page.scroll.to_bottom()
            time.sleep(4)

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

        # 图片的集合
        self.image_set=[]


        for image in images:
            if -1==image.find("originals"):
                continue

            try:
                img = requests.get(image)
                time.sleep(2)
                self.image_set.append([img, image.split('/')[-1]])
                print(image)
            except Exception as e:
                pass

    def download(self, targetUrl='./'):
        if not os.path.exists(targetUrl):
            os.makedirs(targetUrl)

        print('开始下载到本地...')
        for img, suffix in self.image_set:
            with open("{0}/{1}.{2}".format(targetUrl, int(random.random()*1e12), suffix.split('.')[-1]), mode="wb") as f:
                f.write(img.content)
                print('正在下载: {}'.format(f.name))


if __name__ == '__main__':
    pin = PinterestImageSet()
    pin.search('Sousou no frieren')
    pin.download(r'C://sousou/')