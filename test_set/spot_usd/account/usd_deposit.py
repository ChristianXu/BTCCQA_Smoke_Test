__author__ = 'sara'

import unittest
import comm
from time import sleep
import logging
import test_set.spot_usd.bsnsCommon as bcomm

logger = logging.getLogger()
get_element = comm.get_element
get_url = comm.get_url


class USD_Deposit(unittest.TestCase):

    def setUp(self):
        comm.open_url(get_url("exchange"))

        bcomm.login("xukangtest@yopmail.com", "test1234")

        comm.open_url(get_url("exchange_usd_deposit"))

    def test(self):
        get_element("exchange", "sign_in_btn").click()

        get_element("exchange", "email").send_keys("123490904@qq.com")
        get_element("exchange", "password").send_keys("Jasmine621")

        get_element("exchange", "login_btn").click()
        sleep(5)

        comm.open_url("https://exchange.btcc.com/account/deposit/usd/bank")

    def tearDown(self):
        pass
