import logging
import os.path

from celery import shared_task
from django.conf import settings
from pytrends.request import TrendReq

import pandas as pd
from apps.crawler.models import Trend
from sqlalchemy import create_engine


logger = logging.getLogger(__name__)


@shared_task
def fetch_trends():
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'top-search-keywords.csv'))
    variables = [v[0] for v in df.values.tolist()]

    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST")
    db_name = os.environ.get("POSTGRES_DB")
    database_url = f'postgresql://{user}:{password}@{host}:5432/{db_name}'
    engine = create_engine(database_url)
    pytrends = TrendReq(hl='en-US', tz=360)
    for index in range(0, len(variables), 5):
        # we can get the data for max 5 keywords per request.
        kw_list = variables[index:index+5]
        logger.info(f"get data for {kw_list}")
        pytrends.build_payload(kw_list, cat=0, timeframe='now 4-H')

        data = pytrends.interest_over_time()
        data = data.reset_index()
        data = data.drop(columns='isPartial')

        model_df = pd.melt(data, id_vars='date')
        model_df.to_sql(Trend._meta.db_table, if_exists='append', con=engine, index=False)
