import logging

import pandas as pd
from django_pandas.io import read_frame
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crawler.models import Trend

logger = logging.getLogger(__name__)


class TrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword")
        data = Trend.objects.all()
        if keyword:
            data = data.filter(variable=keyword)
        data = data.order_by('-value')
        df = read_frame(data, fieldnames=['date', 'variable', 'value'])
        if keyword:
            df = df.drop('variable', axis=1)
            df['date'] = pd.to_datetime(df['date']).astype(str)
            df = df.set_index('date').astype(str)
            # FIXME: As we need to send the response in {datetime: search_interest, datetime: search_interest...} format
            # we can't actually sort the dict, we need to change the response to format like
            # [{datetime: search_interest}, {datetime: search_interest}, ...]
            df = df.sort_values(by='value', ascending=False).to_dict()['value']
        return Response(data=df)
