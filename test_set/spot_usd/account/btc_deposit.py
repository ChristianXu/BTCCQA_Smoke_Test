__author__ = 'sara'

import unittest
import logging
import comm
import pyperclip
import test_set.spot_usd.bsnsCommon as bcomm

logger = logging.getLogger()

get_element = comm.get_element
get_url = comm.get_url
driver = comm.get_driver()


class BTC_Deposit(unittest.TestCase):

    def setUp(self):
        logger.info("START TEST BTC_Deposit")
        comm.open_url(get_url("exchange"))

        bcomm.login("xukangtest@yopmail.com", "test1234")
        comm.open_url(get_url("exchange_btc_deposit"))

    def test(self):

        value = get_element("deposit", "generate_address").is_enabled()
        print(value)

        get_element("deposit", "copy_address").click()

        value = pyperclip.paste()

        address = get_element("deposit", "address_line").text

        self.assertEqual(value, address)

    def tearDown(self):
        pass