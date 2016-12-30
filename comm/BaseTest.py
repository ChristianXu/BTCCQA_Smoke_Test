__author__ = 'sara'

import unittest
import comm
import logging


class BaseTest(unittest.TestCase):

    def setUp(self):
        # super(BaseTest, self).__init__(self)
        self.get_element = comm.get_element
        self.get_elements = comm.get_elements
        self.get_url = comm.get_url
        self.logger = logging.getLogger()
        self.driver = comm.get_driver()





