__author__ = 'sara'
from comm import BaseTest
from comm import my_assert
from comm import get_url
from comm import open_url
from time import sleep
import test_set.btcc.bsnsCommon as bcomm


class TestHomepage(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        open_url(get_url("homepage"))

    def test01(self):

        bcomm.login(self.user.get("email"), self.user.get("password"))

        self.check_result()

    def check_result(self):

        sleep(2)

        # 检查登陆后的账户 显示是否正确
        value = self.get_element("homepage", "email_text").text

        with my_assert("登陆成功"):
            self.assertEqual(self.user.get("email"), value)

        # 检查btc和ltc价格显示
        btc = self.get_element("homepage", "BTC/CNY_price").text
        with my_assert("balance btc 显示"):
            self.assertNotEqual(btc, "")
        ltc = self.get_element("homepage", "LTC/CNY_price").text
        with my_assert("balance btc 显示"):
            self.assertNotEqual(ltc, "")

        # 检查语言切换
        print("当前语言为===》"+bcomm.get_current_language())

        product_head_first = self.get_element("head", "product").text

        complete_first = self.get_element("homepage", "COMPLETE").text

        product_foot_first = self.get_element("foot", "product").text

        bcomm.switch_language()

        sleep(2)

        product_head_second = self.get_element("head", "product").text

        complete_second = self.get_element("homepage", "COMPLETE").text

        product_foot_second = self.get_element("foot", "product").text

        if bcomm.get_current_language() == "中文":
            with my_assert("检查homepage中英文切换"):
                self.assertEqual(product_head_first, "PRODUCTS")
                self.assertEqual(product_head_second, "产品")
                self.assertEqual(complete_first, "THE COMPLETE")
                self.assertEqual(complete_second, "一站式完整")
                self.assertEqual(product_foot_first, "PRODUCTS")
                self.assertEqual(product_foot_second, "产品")
        else:
            with my_assert("检查homepage中英文切换"):
                self.assertEqual(product_head_second, "PRODUCTS")
                self.assertEqual(product_head_first, "产品")
                self.assertEqual(complete_second, "THE COMPLETE")
                self.assertEqual(complete_first, "一站式完整")
                self.assertEqual(product_foot_second, "PRODUCTS")
                self.assertEqual(product_foot_first, "产品")

    def tearDown(self):
        bcomm.logout()