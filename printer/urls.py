from django.conf.urls import url, include
from .views import CheckCreateView


urlpatterns = [
    url(r'^create_checks/', CheckCreateView.as_view()),
]
urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]


