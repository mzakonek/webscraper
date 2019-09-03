from rest_framework import serializers
from django.shortcuts import get_object_or_404

from scrapers.models import Image, Text, PageUrl


# default field made for serializing lists objects
class StringListField(serializers.ListField):
    child = serializers.CharField()


# main serializer for PageUrl model
class PageUrlSerializer(serializers.ModelSerializer):
    text_scraper = serializers.SerializerMethodField()
    image_scraper = serializers.SerializerMethodField()

    def get_text_scraper(self, url):
        qs = url.texts.first()
        if qs:
            return {'Done at': qs.creationdate}
        return 'Not launched yet'

    def get_image_scraper(self, url):
        qs = url.images.first()
        if qs:
            return {'Done at': qs.creationdate}
        return 'Not launched yet'

    class Meta:
        model = PageUrl
        fields = ('id', 'url', 'text_scraper', 'image_scraper')

    def create(self, validated_data):
        return PageUrl.objects.create(**validated_data)


# main serializer for Text model
class TextSerializer(serializers.ModelSerializer):
    urlname = serializers.ReadOnlyField(source='url.url')

    class Meta:
        model = Text
        read_only = ('urlname',)
        fields = ('urlname', 'creationdate', 'filename',)

    def create(self, validated_data):
        return Text.objects.create(**validated_data)


# serializer for returning text scrapped from Url
class ScrappedTextSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.CharField(max_length=300)
    creationdate = serializers.DateTimeField()
    textfromurl = StringListField()


# serializer for returning url links. Used also with pagination
class ImageSerializer(serializers.ModelSerializer):
    urlname = serializers.ReadOnlyField(source='url.url')

    class Meta:
        model = Image
        fields = ('urlname', 'creationdate', 'imageurl',)

