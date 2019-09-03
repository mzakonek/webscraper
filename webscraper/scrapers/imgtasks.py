import requests
from bs4 import BeautifulSoup
from scrapers.models import Image, PageUrl
from celery import shared_task
import re


@shared_task
def scrap_imgs(pageid):
    page = PageUrl.objects.filter(id=pageid).first()
    res = requests.get(page.url)

    soup = BeautifulSoup(res.text, "html.parser")
    img_tags = soup.find_all("img")

    # patImgSrc = re.compile('src="(.*)".*/>')
    # findPathImgSrc = re.findall(patImgSrc, str(img_tags))

    urls = [img.get('src', '') for img in img_tags]

    # clean data
    for urlindex in range(len(urls)):
        if urls[urlindex].startswith('//'):
            urls[urlindex] = urls[urlindex][2:]

    for imglink in urls:
        Image.objects.create(url=page, imageurl=imglink)

    return 'Done'

    ## CODE FOR SAVING IMAGES LOCALLY
    # import sys
    # import re
    # import urllib.request
    # imgcounter = 0
    # for url in set(urls):
    #     with urllib.request.urlopen(url) as image_on_web:
    #         buf = image_on_web.read()
    #         if "PNG" in str(buf):
    #             with open(str(imgcounter) + '.png', 'wb') as f:
    #                 f.write(buf)
    #         else:
    #             with open(str(imgcounter) + '.jpg', 'wb') as f:
    #                 f.write(buf)
    #         imgcounter += 1


