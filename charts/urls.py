from django.conf.urls import url
from charts.views import index

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^index.html$', index.IndexView.as_view(), name='charts-index'),
    url(r'^chart-json.html$', index.ChartJsonView.as_view(), name='charts-json'),
]
