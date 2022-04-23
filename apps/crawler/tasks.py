import logging

from pytrends.request import TrendReq

import pandas as pd
from apps.crawler.models import Trend
from sqlalchemy import create_engine


logger = logging.getLogger(__name__)


def fetch_trends():
    df = pd.read_csv('top-search-keywords.csv')
    variables = [v[0] for v in df.values.tolist()]

    engine = create_engine('sqlite:///db.sqlite3')
    pytrends = TrendReq(hl='en-US', tz=360)
    for index in range(0, len(variables), 5):
        # we can get the data for max 5 keywords per request.
        kw_list = variables[index:index+5]
        logger.info(f"get data for {kw_list}")
        pytrends.build_payload(kw_list, cat=0, timeframe='now 4-H')

        data = pytrends.interest_over_time()
        data['date'] = data.index.values
        data = data.drop(columns='isPartial')

        model_df = pd.melt(data, id_vars='date')
        model_df.to_sql(Trend._meta.db_table, if_exists='append', con=engine, index=False)
