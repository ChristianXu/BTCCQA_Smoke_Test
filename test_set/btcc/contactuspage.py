__author__ = 'sara'

from comm import BaseTest
from comm import my_assert
from comm import open_url
from comm import get_url
from time import sleep
import test_set.btcc.bsnsCommon as bcomm


class TestContactus(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)
        # self.driver.get(get_url("contact"))
        open_url(get_url("contact"))

    def test_switch_lan(self):
        print("当前语言为===》"+bcomm.get_current_language())

        product_head_first = self.get_element("head", "product").text

        product_foot_first = self.get_element("foot", "product").text

        bcomm.switch_language()

        sleep(1)

        product_head_second = self.get_element("head", "product").text

        product_foot_second = self.get_element("foot", "product").text

        if bcomm.get_current_language() == "中文":
            with my_assert("检查homepage中英文切换"):
                self.assertEqual(product_head_first, "PRODUCTS")
                self.assertEqual(product_head_second, "产品")
                map = self.get_element("contactuspage", "map_img")
                self.assertIsNotNone(map)
                self.assertEqual(product_foot_first, "PRODUCTS")
                self.assertEqual(product_foot_second, "产品")
        else:
            with my_assert("检查homepage中英文切换"):
                self.assertEqual(product_head_second, "PRODUCTS")
                self.assertEqual(product_head_first, "产品")
                map = self.get_element("contactuspage", "map_google")
                self.assertIsNotNone(map)
                self.assertEqual(product_foot_second, "PRODUCTS")
                self.assertEqual(product_foot_first, "产品")