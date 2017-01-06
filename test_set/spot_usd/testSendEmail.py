__author__ = 'sara'


from comm import BaseTest
from comm import my_assert


class TestSend(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

    def test(self):

        with my_assert("测试发邮件"):
            self.assertEqual("!", "1")

    def tearDown(self):
        pass
