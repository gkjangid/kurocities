from django.conf.urls                   import url, include
from django.contrib.auth.decorators     import login_required
from .                                  import views

urlpatterns = [
    url(
        r'^data/(?P<resource_type>.*?)/(?P<resource_id>\d*?)/$',
        login_required( views.Data.as_view() ), name='data',
    ),
    url(
        r'^img/$',
        login_required( views.Image.as_view() ), name='image',
    ),
]
