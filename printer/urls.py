from django.conf.urls import url, include
from .views import CheckCreateView, AvailableCheckView, CheckView


urlpatterns = [
    url(r'^create_checks/', CheckCreateView.as_view(), name='create_checks'),
    url(r'^new_checks/', AvailableCheckView.as_view(), name='new_checks'),
    url(r'^check/', CheckView.as_view(), name='checks'),
]
urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]


