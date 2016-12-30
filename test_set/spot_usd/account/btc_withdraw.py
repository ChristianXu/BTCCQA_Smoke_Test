__author__ = 'sara'

import comm
import logging
import unittest
import random
import test_set.spot_usd.bsnsCommon as bcomm
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException

driver = comm.get_driver()
logger = logging.getLogger()
get_element = comm.get_element
get_elements = comm.get_elements
get_url = comm.get_url


class BTC_Withdraw(unittest.TestCase):

    def setUp(self):
        comm.open_url(get_url("exchange"))

        bcomm.login("xukangtest@yopmail.com", "test1234")

        comm.open_url(get_url("exchange_btc_withdraw"))

    def test(self):

        value = "%.3f" % random.random()
        get_element("withdraw", "btc_amount").send_keys(value)
        get_element("withdraw", "btc_txnpwd").send_keys("test4321")
        get_element("withdraw", "withdraw").click()

        e = get_element("withdraw", "withdraw_loading")

        try:
            while e.is_displayed():
                sleep(1)
        except StaleElementReferenceException:
            pass

        e = get_element("withdraw", "withdraw_msg")

        self.assertEqual(e.text, "Request Success!")
        sleep(5)
        e = get_element("withdraw", "btc_withdraw_table_amount")

        self.assertEqual(e.text, value)

    def tearDown(self):
        driver.quit()
