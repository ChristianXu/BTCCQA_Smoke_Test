__author__ = 'sara'

import unittest
import comm
from time import sleep

get_element = comm.get_element
driver = comm.get_driver()
get_url = comm.get_url


class Logout_User_Access_Landing_Page(unittest.TestCase):

    def setUp(self):
        comm.open_url(get_url("exchange"))

    def test(self):

        get_element("exchange", "check_account").click()
        # sleep(2)

        e = get_element("exchange", "login_form")

        if not e.is_displayed():

            self.fail()

        comm.open_url(get_url("exchange"))

        get_element("exchange", "trade").click()

        handels = driver.window_handles

        driver.switch_to_window(handels[1])

        sleep(1)

        comm.is_page_loaded()

        self.assertEqual(driver.current_url, get_url("exchange_btcusd_trade"))
        driver.close()

        driver.switch_to_window(handels[0])

        get_element("exchange", "how_is_work").click()
        sleep(2)
        if not get_element("exchange", "login_form").is_displayed():

            self.fail()
        sleep(2)

    def tearDown(self):
        pass
