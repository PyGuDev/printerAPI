from django.conf.urls import url
from .views import CheckCreateView


urlpatterns = [
    url(r'^create_checks/', CheckCreateView.as_view()),
]
