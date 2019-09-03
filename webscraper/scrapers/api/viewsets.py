from scrapers.models import PageUrl, Image, Text
from .serializers import PageUrlSerializer, TextSerializer, ScrappedTextSerializer, ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from scrapers.txttasks import scrap_text, save_scrapped_text, read_txt_file
from scrapers.imgtasks import scrap_imgs
from rest_framework.pagination import PageNumberPagination
from celery import current_app
import traceback
import datetime as dt


class PageUrlViewSet(viewsets.ViewSet):
    # create new 'url' record in db
    def create(self, request):
        urlname = request.data['url']
        pages = PageUrl.objects.all()
        page, created = pages.get_or_create(url=urlname)
        if not created:
            return Response({'Page ID': page.id, 'Already created at': page.creationdate})
        serializer = PageUrlSerializer(page)
        return Response(serializer.data)

    # get url details
    def retrieve(self, request, pk=None):
        qs = PageUrl.objects.all()
        page = get_object_or_404(qs, id=pk)
        serializer = PageUrlSerializer(page)
        return Response(serializer.data)


# class made for serializing purpose
class TextFromUrl(object):
    def __init__(self, url, id, creationdate, textfromurl):
        self.id = id
        self.url = url
        self.creationdate = creationdate
        self.textfromurl = textfromurl


class TextViewSet(viewsets.ViewSet):
    # start the process of text scrapping from the url
    def create(self, request):
        # make sure this url exists in the db
        qs = PageUrl.objects.all()
        page = get_object_or_404(qs, id=request.query_params.get('urlid'))

        # now it holds only 1 txtfile for each url, but it should be able to save more,
        # as websites and ads on them are changing very often
        # now = dt.datetime.now()
        try:
            # get text from the page
            data = scrap_text(page.url)
            # save with name '{page.id}.txt' in the folder with all txt files
            filename = save_scrapped_text(data, page.id)
        except:
            print(traceback.format_exc())
            return Response({'detail': 'Error when processing text from url'}), 404

        text, created = Text.objects.all().get_or_create(url=page)
        if not created:
            # if already exists, then update only creationdate in the current Text instance (simplified version for now)
            text.creationdate = dt.datetime.now()
            text.save()
        serializer = TextSerializer(text)

        return Response(serializer.data)

    # get the text that was scrapped from url and get it, if scrapping process is done
    def retrieve(self, request, pk=None):
        text = get_object_or_404(Text.objects.select_related(), url__id=pk)
        # read txt file in which text from url was saved
        data = read_txt_file(text.filename)
        scrappedtext = TextFromUrl(id=text.id, url=text.url.url, creationdate=text.creationdate, textfromurl=data)
        serializer = ScrappedTextSerializer(scrappedtext)
        return Response(serializer.data)


class ImageViewSet(viewsets.ViewSet):
    # start the process of image scrapping from the url
    def create(self, request):
        # make sure this url exists in the db
        qs = PageUrl.objects.all()
        page = get_object_or_404(qs, id=request.query_params.get('urlid'))

        # run task for scrapping imgs from url
        task = scrap_imgs.delay(page.id)
        # save task id in page obj
        page.imgtask_id = task.id
        page.save()

        return Response({'task_id': task.id, 'task_status': task.status})

    # get the links to images scrapped from the url
    def retrieve(self, request, pk=None):
        qs = PageUrl.objects.all()
        page = get_object_or_404(qs, id=pk)

        if not page.imgtask_id:
            return Response({'detail': 'Imgs scrapper process were not initialized for this url yet.'})

        task = current_app.AsyncResult(page.imgtask_id)
        if task.status != "SUCCESS":
            return Response({'task_status': task.status})

        # otherwise process is done, so return resulst
        links = get_list_or_404(Image.objects.select_related(), url__id=pk)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(links, request)
        serializer = ImageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

