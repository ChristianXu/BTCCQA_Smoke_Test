__author__ = 'sara'

from comm import BaseTest
from comm import my_assert
from comm import get_url
from comm import open_url
from time import sleep
import test_set.btcc.bsnsCommon as bcomm


class TestPropage(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        open_url(get_url("propage"))

    def test_pro_switch_lan(self):
        sleep(3)
        print("当前语言为===》"+bcomm.get_current_language())

        product_head_first = self.get_element("head", "product").text

        cny_trading_first = self.get_element("propage", "cny_trading").text

        product_foot_first = self.get_element("foot", "product").text

        bcomm.switch_language()

        print("当前语言为===》"+bcomm.get_current_language())

        sleep(1)

        product_head_second = self.get_element("head", "product").text

        cny_trading_second = self.get_element("propage", "cny_trading").text

        product_foot_second = self.get_element("foot", "product").text

        if bcomm.get_current_language() == "中文":
            with my_assert("检查propage中英文切换"):
                self.assertEqual(product_head_first, "PRODUCTS")
                self.assertEqual(product_head_second, "产品")
                self.assertEqual(cny_trading_first, "CNY Trading\nCNY Trading")
                self.assertEqual(cny_trading_second, "人民币交易市场\n人民币交易市场")
                self.assertEqual(product_foot_first, "PRODUCTS")
                self.assertEqual(product_foot_second, "产品")
        else:
            with my_assert("检查propage中英文切换"):
                self.assertEqual(product_head_second, "PRODUCTS")
                self.assertEqual(product_head_first, "产品")
                self.assertEqual(cny_trading_second, "CNY Trading\nCNY Trading")
                self.assertEqual(cny_trading_first, "人民币交易市场\n人民币交易市场")
                self.assertEqual(product_foot_second, "PRODUCTS")
                self.assertEqual(product_foot_first, "产品")

    def test_cny_trading(self):
        self.get_element("propage", "cny_trading").click()

        sleep(3)
        # handels = self.driver.window_handles
        # self.driver.switch_to_window(handels[1])
        # sleep(2)
        url = self.driver.current_url

        with my_assert("点击cny_trading 进入trading 页面"):
            self.assertEqual(url, get_url("propage_cny_trading"))

        # 关闭导航
        self.get_element("propage_cny_trade", "note_confirm_btn").click()
        sleep(1)
        self.get_element("propage_cny_trade", "guide_colse_btn").click()
        sleep(1)

        # 检查语言切换
        self.get_element("propage_cny_trade", "trade_current_language_div").click()

        # 切换英文
        self.get_element("propage_cny_trade", "trade_en_language").click()
        sleep(1)
        value = self.get_element("propage_cny_trade", "order_book").text

        with my_assert("cny_trading 切换英文"):
            self.assertEqual(value, "ORDER BOOK")

        self.get_element("propage_cny_trade", "trade_current_language_div").click()

        # 切换中文
        self.get_element("propage_cny_trade", "trade_ch_language").click()

        sleep(1)
        value = self.get_element("propage_cny_trade", "order_book").text

        with my_assert("cny_trading 切换中文"):
            self.assertEqual(value, "盘口")