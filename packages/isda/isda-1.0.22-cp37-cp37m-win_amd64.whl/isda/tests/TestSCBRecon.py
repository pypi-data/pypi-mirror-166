import os

os.environ['ENVIRONMENT'] = 'prod'

import logging
import unittest
import datetime

import pandas as pd

import sqlalchemy
from sqlalchemy.sql import text
from ogamdatamodels.orm.session_scope import connection_string_dwh

from loan.core.engine.deal_facility_utils import DealFacilityEngineEmptyDealException


def load_scb_trade(trade_date, quotation_type='Flat Spread (bps)') -> pd.DataFrame:
    """
    load the daily scb flat spread dataset into pandas
    :param cob_date:
    :param deal_id:
    :return: pandas.DataFrame fff
    throw; DealFacilityEngineEmptyDealException
    """

    # look up all the current deal facilities on this date.
    engine = sqlalchemy.create_engine(
        connection_string_dwh, fast_executemany=True)
    with engine.connect() as conn:
        sql = f"""SELECT [quote] * 10000 as [quote_in_bps]
                  , [traded_notional]/1e6 as [notional]
                  , [trade_date]
                  , [first_coupon_date]
                  , [maturity]
                  , [coupon] * 10000.0 as [coupon]
                  , [direction]
                  , [accrued]
                  , [clean_settlement_amount]
                  , [dirty_settlement_amount]
                  , [settlement_ccy]
                  , [instrument_id]
                  , 0.4 as [recovery_rate]
              FROM [SCB_Blotter].[orm].[scb_trade_universe_view2] where [trade_date] = :trade_date and quotation_type = :quotation_type"""
        logging.debug(sql)
        df0 = pd.read_sql(text(sql), con=conn, params={"trade_date": trade_date, "quotation_type": quotation_type})

        if df0.empty:
            raise DealFacilityEngineEmptyDealException(
                f'load_scb_trade empty for {trade_date} and {quotation_type} ')

    return df0


class MyTestCase(unittest.TestCase):
    def test_something(self):
        trade_date = datetime.datetime(2022, 8, 31)
        df = load_scb_trade(trade_date)
        print(df)

        def add(row):
            return row[0] + row[1] + row[2]

        df['new_col'] = df.apply(add, axis=1)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
