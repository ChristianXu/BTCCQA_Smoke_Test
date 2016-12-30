# -*- coding: utf-8 -*-
__author__ = 'sara'


import unittest
import sys
import io


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        lines = map(lines)
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.outputBuffer = io.StringIO()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

import datetime
import xlsxwriter


class EXCELTestRunner:

    def __init__(self, report_name, project_name, version, log_path=None, verbosity=1):
        self.name = report_name
        self.project_name = project_name
        self.version = version
        self.verbosity = verbosity
        self.workbook = xlsxwriter.Workbook(self.name)
        self.workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        self.workbook.add_format({}).set_border(1)
        self.startTime = datetime.datetime.now()

    def _get_format_center(self):
        return self.workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})

    def _set_border_(self):
        return self.workbook.add_format({}).set_border(1)

    def _create_total(self):
        worksheet = self.workbook.add_worksheet(u"测试报告概览")
        self.title_format = self.workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True, 'font_size':24})
        worksheet.merge_range("B2:E2", u"测试报告概览", self.title_format)
        worksheet.write("B3", u"项目名称", self._get_format_center())
        worksheet.write("C3", self.project_name, self._get_format_center())
        worksheet.write("B4", u"版本", self._get_format_center())
        worksheet.write("C4", self.version, self._get_format_center())
        worksheet.write("B5", u"开始时间", self._get_format_center())
        worksheet.write("C5", str(self.startTime), self._get_format_center())
        worksheet.write("B6", u"结束时间", self._get_format_center())
        worksheet.write("C6", str(self.stopTime), self._get_format_center())
        worksheet.write("D3", u"用例总数", self._get_format_center())
        worksheet.write_url("D4", u"internal:通过用例详情!A1", cell_format=self._get_format_center(), string=u"成功总数")
        worksheet.write_url("D5", u"internal:失败用例详情!A1", cell_format=self._get_format_center(), string=u"失败总数")
        worksheet.write_url("D6", u"internal:错误用例详情!A1", cell_format=self._get_format_center(), string=u"错误总数")
        worksheet.write("D7", u"成功率", self._get_format_center())
        worksheet.write("B7", u"经过时间(ms)", self._get_format_center())
        worksheet.write("C7", str(self.stopTime-self.startTime), self._get_format_center())

        return worksheet

    def _create_pie(self, worksheet):

        chart_pie = self.workbook.add_chart({'type': 'pie'})

        chart_pie.add_series({
            'name':       u'case运行结果统计',
            'categories': u'=测试报告概览!$D$4:$D$6',
            'values': u'=测试报告概览!$E$4:$E$6',
            'points': [
                {'fill': {'color': '#5ABA10'}},
                {'fill': {'color': '#FE110E'}},
                {'fill': {'color': '#CA5C05'}},
            ],
        })

        chart_pie.set_style(10)

        chart_pie.set_title({'name': u'case运行结果统计'})

        worksheet.insert_chart('C10', chart_pie, {'x_offset': 25, 'y_offset': 10})

    def _create_case(self, sheet_name):
        worksheet = self.workbook.add_worksheet(sheet_name)
        worksheet.merge_range("B2:E2", sheet_name, self.title_format)
        worksheet.write("B3", u"用例名称", self._get_format_center())
        worksheet.write("C3", u"用例描述", self._get_format_center())
        worksheet.write("D3", u"预期", self._get_format_center())
        worksheet.write("E3", u"实际", self._get_format_center())

        return worksheet

    def sort_result(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def _write_data(self, result):
        total_worksheet = self._create_total()

        pass_worksheet = self._create_case(u"通过用例详情")
        fail_worksheet = self._create_case(u"失败用例详情")
        error_worksheet = self._create_case(u"错误用例详情")

        pass_rows = fail_rows = error_rows = 3
        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # subtotal for a class
            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            # doc = cls.v and cls.__doc__.split("\n")[0] or ""
            # case_name = doc and '%s: %s' % (name, doc) or name
            case_name = name

            for n, t, o, e in cls_results:
                name = t.id().split('.')[-1]
                doc = t.shortDescription() or ""
                desc = doc and ('%s: %s' % (name, doc)) or name

                # o and e should be byte string because they are collected from stdout and stderr?
                if isinstance(o,str):
                    # TODO: some problem with 'string_escape': it escape \n and mess up formating
                    # uo = unicode(o.encode('string_escape'))
                    uo = e
                else:
                    uo = o
                if isinstance(e,str):
                    # TODO: some problem with 'string_escape': it escape \n and mess up formating
                    # ue = unicode(e.encode('string_escape'))
                    ue = e
                else:
                    ue = e

                if n == 0:
                    pass_worksheet.write(pass_rows, 1, case_name, self._get_format_center())
                    pass_worksheet.write(pass_rows, 2, desc, self._get_format_center())
                    pass_rows += 1
                elif n == 1:
                    fail_worksheet.write(fail_rows, 1, case_name, self._get_format_center())
                    fail_worksheet.write(fail_rows, 2, desc, self._get_format_center())
                    fail_worksheet.write(fail_rows, 3, uo+ue, self._get_format_center())
                    fail_rows += 1
                else:
                    error_worksheet.write(error_rows, 1, case_name, self._get_format_center())
                    error_worksheet.write(error_rows, 2, desc, self._get_format_center())
                    error_worksheet.write(error_rows, 3, uo+ue, self._get_format_center())
                    error_rows += 1

        total = result.success_count+result.failure_count+result.error_count
        total_worksheet.write("E3", total,
                              self._get_format_center())
        total_worksheet.write("E4", result.success_count,
                              self._get_format_center())
        total_worksheet.write("E5", result.failure_count,
                              self._get_format_center())
        total_worksheet.write("E6", result.error_count,
                              self._get_format_center())

        percent = "%.2f%%" % (float(result.success_count)/float(total)*100)

        total_worksheet.write("E7", percent,
                              self._get_format_center())

        self._create_pie(total_worksheet)

        self.workbook.close()

    def run(self, test):
        """
        Run the given test case or test suite.
        :param test:
        :return:
        """
        result = _TestResult(self.verbosity)

        test(result)
        self.stopTime = datetime.datetime.now()
        self._write_data(result)
        print(sys.stderr, '\nTime Elapsed: %s' % (self.stopTime-self.startTime))
        return result


