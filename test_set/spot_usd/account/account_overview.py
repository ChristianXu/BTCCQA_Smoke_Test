__author__ = 'sara'

import unittest
import comm
import logging
import test_set.spot_usd.bsnsCommon as bcomm

from time import sleep

get_element = comm.get_element
get_url = comm.get_url
logger = logging.getLogger()
driver = comm.get_driver()


class Account_Overview(unittest.TestCase):

    def setUp(self):

        comm.open_url(get_url("exchange"))
        bcomm.login("xukangtest@yopmail.com", "test1234")

    def test(self):

        get_element("exchange", "check_account").click()

        sleep(3)

        self.assertEqual(driver.current_url, get_url("exchange_account"))

        get_element("account", "trade_now").click()

        self.assertEqual(driver.current_url, get_url("exchange_btcusd_trade"))

        driver.back()
        get_element("account", "deposit_USD").click()
        self.assertEqual(driver.current_url, get_url("exchange_usd_deposit"))

        driver.back()
        get_element("account", "withdraw_USD").click()
        self.assertEqual(driver.current_url, get_url("exchange_usd_withdraw"))

        driver.back()
        get_element("account", "deposit_BTC").click()
        self.assertEqual(driver.current_url, get_url("exchange_btc_deposit"))

        driver.back()
        get_element("account", "withdraw_BTC").click()
        self.assertEqual(driver.current_url, get_url("exchange_btc_withdraw"))

    def tearDown(self):
        driver.quit()
