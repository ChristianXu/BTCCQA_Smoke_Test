__author__ = 'sara'

import comm
import logging
import unittest
import test_set.spot_usd.bsnsCommon as bcomm
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

driver = comm.get_driver()
logger = logging.getLogger()
get_element = comm.get_element
get_elements = comm.get_elements
get_url = comm.get_url


class Add_Address(unittest.TestCase):

    def setUp(self):
        comm.open_url(get_url("exchange"))

        bcomm.login("xukangtest@yopmail.com", "test1234")

        comm.open_url(get_url("exchange_btc_cards_setting"))

        self.count_address = len(get_elements("manage_address_book", "address_table_tr"))

    def test(self):

        get_element("manage_address_book", "address").send_keys("mkGkiDjUpQvDs7Me1JUaTmmpBfgxjk6bm2")

        get_element("manage_address_book", "address_label").send_keys("test")

        get_element("manage_address_book", "verification_code").send_keys("110609")

        get_element("manage_address_book", "add_address_btn").click()

        e = get_element("manage_address_book", "add_address_loading")

        try:
            while e.is_displayed():
                sleep(1)
        except StaleElementReferenceException:
            pass

    def tearDown(self):

        comm.open_url("https://exchange-staging.btcc.com/account/withdraw/btc/cards-setting")
        sleep(4)
        count_address = len(get_elements("manage_address_book", "address_table_tr"))

        self.assertEqual(self.count_address+1, count_address)

        get_element("manage_address_book", "delete_address").click()

        sleep(3)

        driver.quit()

