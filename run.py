__author__ = 'sara'

import os
import unittest
import comm
import logging

logger = logging.getLogger()
resultPath = os.path.join(comm.log_path, "report.xls")


class Alltest():

    def __init__(self):
        self.caseListPath = os.path.join(comm.prjDir, "config", "testCases.txt")
        self.caseList = []

    def set_case_list(self):
        """from the caseList get the caseName,set in caseList
        :return:
        """
        fp = open(self.caseListPath)

        for data in fp.readlines():

            s_data = str(data)
            if s_data != '' and not s_data.startswith("#"):
                self.caseList.append(s_data.replace("\n", ""))
        fp.close()

    def get_case_path(self):

        return os.path.join(comm.prjDir, "test_set", "btcchina")

    def create_suite(self):
        """from the caseList,get caseName,According to the caseName to search the testSuite
        :return:test_suite
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module_list = []

        if len(self.caseList) > 0:

            for case_name in self.caseList:

                discover = unittest.defaultTestLoader.discover(self.get_case_path(), pattern=case_name+'.py', top_level_dir=None)
                suite_module_list.append(discover)

        if len(suite_module_list) > 0:

            for suite in suite_module_list:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """run test
        :return:
        """
        try:
            suite = self.create_suite()
            if suite is not None:
                logger.info("Start to test")
                runner = unittest.TextTestRunner()
                runner.run(suite)
                # fp = open(resultPath, 'wb')
                # runner = HTMLTestRunner(stream=fp, title='testReport', description='Report_description', verbosity=2)
                # runner.run(suite)
                # runner = comm.EXCELTestRunner(resultPath, "test", "v1.0")
                # runner.run(suite)
                logger.info("End to test")
            else:
                logger.info("Have no case to run")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            s = comm.SendEmail()
            s.send()

if __name__ == '__main__':

    ojb = Alltest()
    ojb.run()
