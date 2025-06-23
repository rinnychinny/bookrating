from rest_framework.routers import DefaultRouter
from .views_api import (WorkViewSet,
                        AuthorViewSet,
                        BookEditionViewSet,
                        WorkAuthorViewSet,
                        RatingViewSet)

router = DefaultRouter()
router.register(r'works', WorkViewSet, basename='work')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'editions', BookEditionViewSet, basename='edition')
router.register(r'work-authors', WorkAuthorViewSet, basename='workauthor')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = router.urls
