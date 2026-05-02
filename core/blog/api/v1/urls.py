from rest_framework.routers import DefaultRouter
from . import views

app_name = "v1"

router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")
router.register("categories", views.CategoryViewSet, basename="category")

urlpatterns = router.urls
