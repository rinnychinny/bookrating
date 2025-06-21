from rest_framework.routers import DefaultRouter
from .views_api import WorkViewSet, AuthorViewSet, BookEditionViewSet

router = DefaultRouter()
router.register(r'works', WorkViewSet, basename='work')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'editions', BookEditionViewSet, basename='edition')

urlpatterns = router.urls
