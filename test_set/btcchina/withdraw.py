__author__ = 'sara'
from comm import BaseTest
from comm import my_assert
from comm import get_url
from comm import open_url
from time import sleep
import test_set.btcchina.bsnsCommon as bcomm


class TestWithdraw(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        open_url(get_url("homepage"))
        bcomm.login(self.user.get("email"), self.user.get("password"))

    def test_withdraw_btc(self):
        open_url(get_url("withdraw_btc"))
        sleep(2)
        self.get_element("withdraw", "withdraw_amount").send_keys("0.001")
        self.get_element("withdraw", "withdraw_trans_password").send_keys(self.user.get("trans_password"))
        sleep(1)
        self.get_element("withdraw", "withdraw_btn").click()
        sleep(0.1)
        while self.get_element("withdraw", "withdraw_btn_loading") is not None:
            sleep(1)

        sleep(3)

        with my_assert("提现 btc"):
            self.assertTrue(self.get_element("withdraw", "success_msg").is_displayed())
        self.get_element("withdraw", "cancel").click()
        sleep(1)

        self.get_element("withdraw", "confirm").click()

        while self.get_element("withdraw", "confirm_loading") is not None:
            sleep(1)

    def tearDown(self):
        self.driver.get(get_url("homepage"))
        bcomm.logout()
