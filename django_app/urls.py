#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import include, url
# from .views import misc, landing, description, input, output, batch, ctsGenerateReport
# from .cts_api.views import test_ws_page
# from views import history, algorithms, references, qaqc
from . import views

urlpatterns = [
    url(r'^testing/', views.test_page),
]