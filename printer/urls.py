from django.conf.urls import url, include
from .views import CheckCreateView, AvailableCheckView, CheckView


urlpatterns = [
    url(r'^create_checks/', CheckCreateView.as_view()),
    url(r'^new_checks/', AvailableCheckView.as_view()),
    url(r'^check/', CheckView.as_view()),
]
urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]


