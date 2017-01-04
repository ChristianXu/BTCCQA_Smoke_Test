__author__ = 'sara'


from comm import BaseTest
from comm import my_assert
from comm import get_url
from comm import open_url
from time import sleep
import random
import test_set.btcchina.bsnsCommon as bcomm


class TestDeposit(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        open_url(get_url("homepage"))
        bcomm.login("protestaccount002", "btcchinA1")

    def test_deposit_cny(self):
        open_url(get_url("deposit_cny"))
        sleep(2)
        self.get_element("deposit", "select_bank").click()
        sleep(1)
        self.get_element("deposit", "first_bank").click()
        sleep(1)
        self.get_element("deposit", "amount").send_keys(self.get_random())
        amount = self.get_element("deposit", "amount").get_attribute("value")
        amount_decimal = self.get_element("deposit", "amount-decimal").text
        value = amount+amount_decimal
        print("========> "+value)
        self.get_element("deposit", "create_request").click()
        while self.get_element("deposit", "create_request_loading") is not None:
            sleep(1)
        sleep(2)
        with my_assert(u"充值 cny"):
            value2 = self.get_element("deposit", "transfer_info_amount").text
            self.assertEqual(value, value2.replace(",", ""))
        print(self.get_element("deposit", "close"))

        while self.get_element("deposit", "close").is_displayed():

            self.get_element("deposit", "close").click()
            sleep(2)
        while self.get_element("deposit", "cancel").is_displayed():
            self.get_element("deposit", "cancel").click()
            sleep(2)
            if self.get_element("deposit", "confirm_cancel").is_displayed():
                self.get_element("deposit", "confirm_cancel").click()
                sleep(2)
                break

    def test_deposit_btc(self):
        open_url(get_url("deposit_btc"))
        sleep(3)
        with my_assert(u"充值 btc 检查二维码显示"):
            self.assertIsNotNone(self.get_element("deposit", "btc_qrcode"))

        with my_assert(u"充值 btc 检查地址显示"):
            self.assertIsNotNone(self.get_element("deposit", "btc_address"))

    def get_random(self):
        return str(random.randint(100, 10000))

    def tearDown(self):
        self.driver.get(get_url("homepage"))
        bcomm.logout()
