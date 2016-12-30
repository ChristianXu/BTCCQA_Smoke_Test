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
get_url = comm.get_url


class USD_Withdraw(unittest.TestCase):

    def setUp(self):
        comm.open_url(get_url("exchange"))

        bcomm.login("xukangtest@yopmail.com", "test1234")

        comm.open_url(get_url("exchange_account"))

    def test(self):
        usd_balance = (get_element("account", "balance_USD").text).replace(",", "")

        comm.open_url(get_url("exchange_usd_withdraw"))

        name = get_element("withdraw", "usd_name").text

        self.assertEqual(name, "KANG XU")

        balance = float(usd_balance) / 1.001

        dot_index = str(balance).index(".")

        a_balance = str(balance)[:dot_index+3]

        available_balance = (get_element("withdraw", "usd_balance").text).replace(",", "")

        self.assertEqual(a_balance, available_balance)

        value = "%.2f" % random.random()

        get_element("withdraw", "usd_amount").send_keys(value)

        get_element("withdraw", "usd_txnpwd").send_keys("test4321")

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

        e = get_element("withdraw", "usd_withdraw_table_amount")

        self.assertEqual(e.text, value)

    def tearDown(self):
        driver.quit()
