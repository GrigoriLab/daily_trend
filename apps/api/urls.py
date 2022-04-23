from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from apps.api.v1.trend import TrendView

apipatterns = [
    path("trends/", TrendView.as_view(), name='trends'),
    path('auth/', obtain_auth_token, name='auth'),
]


urlpatterns = [
    path("v1/", include(apipatterns)),
]
