# -*- coding: utf-8 -*-
__author__ = 'sara'

import yaml
import os
import platform
import comm
import unittest
from selenium import webdriver
from multiprocessing.pool import Pool


prjDir = comm.prjDir
config_path = os.path.join(prjDir, "config")
driver_path = os.path.join(config_path, "driver")
test_case_path = os.path.join(config_path, "testCases.yaml")
cases_path = os.path.join(prjDir, "test_set")

OS = platform.system()
WEB_DRIVER = {}
if OS == "Darwin":
    WEB_DRIVER = {
        "chrome": os.path.join(driver_path, "chromedriver"),
        "firefox": os.path.join(driver_path, "geckodriver"),

    }
else:
    WEB_DRIVER = {
        "chrome": os.path.join(driver_path, "chromedriver.exe"),
        "firefox": os.path.join(driver_path, "geckodriver.exe"),

    }

BROWSER = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
}


class Init:

    def __init__(self):
        pass

    def get_test_case(self):
        cases = {}
        with open(test_case_path, encoding='utf8') as f:
            data = yaml.load(f)

            for d in data.keys():
                if data.get(d).get("test_case") is None:
                    continue
                cases[d] = data.get(d)

        return cases

    def run(self):
        cases = self.get_test_case()
        pool = Pool(processes=len(cases))
        result = []

        for key, value in cases.items():

            result.append(pool.apply_async(self.init_driver, args=(key, value)))

        pool.close()
        pool.join()

        for res in result:
            print(":::", res.get())

    def init_driver(self, website, info):
        browser = info.get("browser")
        web_driver = WEB_DRIVER.get(browser)
        browser_class = BROWSER.get(browser)
        driver = browser_class(executable_path=web_driver)
        driver.maximize_window()
        driver.set_page_load_timeout(120)
        comm.Info.set_info(website, info.get("user"), driver)

        self.run_test(self.create_suite(website, info.get("test_case")))

    def run_test(self, case_suite):
        runner = unittest.TextTestRunner()
        runner.run(case_suite)

        send = comm.SendEmail()
        send.send()

    def create_suite(self, website, cases):
        """from the caseList,get caseName,According to the caseName to search the testSuite
        :return:test_suite
        """
        test_suite = unittest.TestSuite()
        suite_module_list = []
        find_path = os.path.join(cases_path, website)

        for case_name in cases:

            discover = unittest.defaultTestLoader.discover(find_path, pattern=case_name+'.py', top_level_dir=None)
            suite_module_list.append(discover)

        for suite in suite_module_list:
            for test_name in suite:
                test_suite.addTest(test_name)

        return test_suite


if __name__ == "__main__":
    d = Init()
    d.run()
