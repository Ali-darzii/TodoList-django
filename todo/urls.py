from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'todos', views.TodosViewSet, basename='todos')


urlpatterns = [] + router.urls
