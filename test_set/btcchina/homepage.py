__author__ = 'sara'

from comm import BaseTest
from comm import my_assert
from comm import get_url
from time import sleep
import test_set.btcchina.bsnsCommon as bcomm


class TestHomepage(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        self.driver.get(get_url("homepage"))

    def test(self):

        bcomm.login(self.user.get("email"), self.user.get("password"))

        self.check_result()

    def check_result(self):

        sleep(2)

        # 检查登陆后的账户 显示是否正确
        value = self.get_element("homepage", "email_text").text
        # value = 'ken***@gmail.com'

        with my_assert("登陆成功"):
            self.assertEqual('ken***@gmail.com', value)

        # 检查页面跳转是否正常
        self.get_element("homepage", "trade").click()
        sleep(1)
        url = self.driver.current_url
        with my_assert("点击trade链接跳转"):
            self.assertEqual(url, get_url("trade"))
        self.driver.back()
        sleep(2)
        self.get_element("homepage", "market_trend").click()
        sleep(1)
        url = self.driver.current_url
        with my_assert("点击market Trend 链接跳转"):
            self.assertEqual(url, get_url("market_trend"))
        self.driver.back()

        sleep(2)
        self.get_element("homepage", "help_center").click()
        handels = self.driver.window_handles
        self.driver.switch_to_window(handels[1])
        sleep(2)
        url = self.driver.current_url
        with my_assert("点击help center 链接跳转"):
            self.assertEqual(url, get_url("help_center"))

        self.driver.close()
        self.driver.switch_to_window(handels[0])
        sleep(2)

        self.driver.refresh()
        sleep(2)
        self.get_element("homepage", "deposit_withdraw").click()

        url = self.driver.current_url
        with my_assert("点击withdraw deposit链接跳转"):
            self.assertEqual(url, get_url("deposit_cny"))
        self.driver.back()

        sleep(2)
        # 检查账户信息是否显示出来
        total_assets = self.get_element("homepage", "total_assets").text
        with my_assert("total assets 显示"):
            self.assertNotEqual(total_assets, "")

        available = self.get_element("homepage", "available").text
        with my_assert("available 显示"):
            self.assertNotEqual(available, "")

        balance_btc = self.get_element("homepage", "balance_btc").text
        with my_assert("balance btc 显示"):
            self.assertNotEqual(balance_btc, "")

        balance_ltc = self.get_element("homepage", "balance_ltc").text
        with my_assert("balance ltc 显示"):
            self.assertNotEqual(balance_ltc, "")

        # 检查btc/cny 和 ltc/cny的价格是否正常的显示出来
        self.get_element("homepage", "BTC/CNY").click()

        last_price = self.get_element("homepage", "last_price").text
        with my_assert("btc/cny last_price 显示"):
            self.assertNotEqual(last_price, "")

        daily_high = self.get_element("homepage", "daily_high").text
        with my_assert("btc/cny daily_high 显示"):
            self.assertNotEqual(daily_high, "")

        daily_low = self.get_element("homepage", "daily_low").text
        with my_assert("btc/cny daily_low 显示"):
            self.assertNotEqual(daily_low, "")

        self.get_element("homepage", "LTC/CNY").click()

        last_price = self.get_element("homepage", "last_price").text
        with my_assert("ltc/cny last_price 显示"):
            self.assertNotEqual(last_price, "")

        daily_high = self.get_element("homepage", "daily_high").text
        with my_assert("ltc/cny daily_high 显示"):
            self.assertNotEqual(daily_high, "")

        daily_low = self.get_element("homepage", "daily_low").text
        with my_assert("ltc/cny daily_low 显示"):
            self.assertNotEqual(daily_low, "")

    def tearDown(self):
        self.driver.get(get_url("homepage"))
        bcomm.logout()
