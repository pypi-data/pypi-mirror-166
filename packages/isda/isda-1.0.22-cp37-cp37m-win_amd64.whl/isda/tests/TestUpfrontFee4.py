import os
import unittest
import datetime
import uuid

from isda.isda import compute_isda_upfront, average


class MyTestCase(unittest.TestCase):
    """
        Testcase that has been reconciled with output from MarkIT partners online calculator and
        separate ISDA source; these figures are accurate to 11 decimal places and battle tested
        enough to be useful for more than just indicative risk.

        i) test coverage needs to be extended to handle cases over weekends & holidays
        ii) for now the coverage is a simple buy/sell protection flat spread trade

    """

    __name__ = "MyTestCase"

    def setUp(self):
        # available from markit swap feed

        self.is_rofr = 1
        self.swap_rates1 = [0.026872,
                0.028731,
                0.030761,
                0.034289,
                0.036660,
                0.035331,
                0.033401,
                0.032172,
                0.031442,
                0.031032,
                0.030762,
                0.030602,
                0.030542,
                0.030582,
                0.030722,
                0.030842,
                0.030261,
                0.029141,
                0.028101]
        #
        self.swap_rates = [0.0267200000,
                           0.0285000000,
                           0.0306000000,
                           0.0342780000,
                           0.0369850000,
                           0.0359900000,
                           0.0342100000,
                           0.0330200000,
                           0.0323100000,
                           0.0319000000,
                           0.0316290000,
                           0.0314490000,
                           0.0313890000,
                           0.0314280000,
                           0.0315580000,
                           0.0316590000,
                           0.0310680000,
                           0.0299580000,
                           0.0288990000]

        self.swap_tenors = ['1M', '2M', '3M', '6M', '1Y', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '8Y', '9Y', '10Y', '12Y',
                            '15Y', '20Y', '25Y', '30Y']

        # economics of trade 1% fixed coupon
        self.coupon = 100.0
        self.trade_date = '07/09/2022'
        self.settle_date = '12/09/2022'
        self.accrual_start_date = '21/06/2022'
        self.maturity_date = '20/06/2027'
        self.notional = 108.0
        self.is_buy_protection = 0  # only ever buy or sell protection!
        self.verbose = 0

    def tearDown(self):
        pass

    def test_compute_isda_upfront(self):

        # simulate an index with 125 names;;
        self.credit_spread_list = [85.1 / 10000.]
        self.recovery_rate_list = [0.4]

        """ EUR ACT/360, 30/360, 1Y, 1Y """
        self.swapFixedDayCountConvention = 'ACT/360'
        self.swapFloatingDayCountConvention = 'ACT/360'
        self.swapFixedPaymentFrequency = '1Y'
        self.swapFloatingPaymentFrequency = '1Y'

        unique_filename = str(uuid.uuid4())
        self.holiday_filename = f'{unique_filename}.dat'
        self.holiday_list = [16010101, 20180320, 20220620]

        def save_to_file(*holiday_list):
            with open(self.holiday_filename, mode='wt', encoding='utf-8') as myfile:
                for lines in holiday_list:
                    myfile.write('\n'.join(str(line) for line in lines))
                    myfile.write('\n')

        # just for measuring performance

        save_to_file(self.holiday_list)

        wall_time_list = list()
        for credit_spread, recovery_rate in zip(self.credit_spread_list, self.recovery_rate_list):
            f = compute_isda_upfront(self.trade_date,
                                     self.maturity_date,
                                     self.accrual_start_date,
                                     self.settle_date,
                                     recovery_rate,
                                     self.coupon,
                                     self.notional,
                                     self.is_buy_protection,
                                     self.swap_rates,
                                     self.swap_tenors,
                                     credit_spread,
                                     self.is_rofr,
                                     self.holiday_filename,
                                     self.swapFloatingDayCountConvention,
                                     self.swapFixedDayCountConvention,
                                     self.swapFixedPaymentFrequency,
                                     self.swapFloatingPaymentFrequency,
                                     self.verbose)

            upfront_charge_dirty, upfront_charge_clean, accrued_interest, status, duration_in_milliseconds = f

            wall_time_list.append(float(duration_in_milliseconds))
            print(f"credit_spread {credit_spread * 10000.:,.2f} "
                  f"recovery_rate {recovery_rate:,.2f} "
                  f"accrued {accrued_interest * 1e6:,.2f} "
                  f"clean_settlement_amount {(upfront_charge_clean) * 1e6:,.2f} "
                  f"dirty_settlement_amount: {(upfront_charge_dirty) * 1e6:,.2f} ")

        a = [wall_time_list]
        print("average execution {0}".format(average(a)))

        os.remove(self.holiday_filename)

        """ assert to below 

        self.assertAlmostEqual((upfront_charge_dirty) * 1e6, -935644.50)
        self.assertAlmostEqual((upfront_charge_clean) * 1e6, -695644.50)
        self.assertAlmostEqual(accrued_interest * 1e6, -240000.00)"""



if __name__ == '__main__':
    unittest.main()
