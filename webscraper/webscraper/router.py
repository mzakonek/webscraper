from scrapers.api.viewsets import PageUrlViewSet, TextViewSet, ImageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pages', PageUrlViewSet, basename='pages')
router.register('textscraper', TextViewSet, basename='textscraper')
router.register('imgscraper', ImageViewSet, basename='imgscraper')
