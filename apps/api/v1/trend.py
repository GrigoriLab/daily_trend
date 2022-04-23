import logging

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crawler.models import Trend
from django_pandas.io import read_frame

logger = logging.getLogger(__name__)


class TrendView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        data = Trend.objects.all()
        df = read_frame(data, fieldnames=['date', 'variable', 'value'])
        return Response(df)
