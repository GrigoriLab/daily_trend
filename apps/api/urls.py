from django.urls import include, path
from apps.api.v1.trend import TrendView

apipatterns = [
    path("trends/", TrendView.as_view(), name='trends'),
]


urlpatterns = [
    path("v1/", include(apipatterns)),
]
