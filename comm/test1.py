__author__ = 'sara'


from macaca import WebDriver
import time
import threading
import requests
from requests.exceptions import ReadTimeout
from multiprocessing.pool import Pool
import os
import re

class InitDevice:
    """
    获取连接的设备的信息
    """
    def __init__(self):
        self.GET_ANDROID = "adb devices"
        self.GET_IOS = "instruments -s devices"

    def get_device(self):
        value = os.popen(self.GET_ANDROID)

        device = []

        for v in value.readlines():
            android = {}
            s_value = str(v).replace("\n", "").replace("\t", "")
            if s_value.rfind('device') != -1 and (not s_value.startswith("List")) and s_value != "":
                android['platformName'] = 'Android'
                android['udid'] = s_value[:s_value.find('device')].strip()
                android['package'] = 'com.btcc.mobi'
                android['activity'] = 'com.btcc.mobi.module.welcome.LaunchActivity'
                device.append(android)

        value = os.popen(self.GET_IOS)

        for v in value.readlines():
            iOS = {}

            s_value = str(v).replace("\n", "").replace("\t", "").replace(" ", "")

            if v.rfind('Simulator') != -1:
                continue
            if v.rfind("(") == -1:
                continue

            iOS['platformName'] = 'iOS'
            iOS['platformVersion'] = re.compile(r'\((.*)\)').findall(s_value)[0]
            iOS['deviceName'] = re.compile(r'(.*)\(').findall(s_value)[0]
            iOS['udid'] = re.compile(r'\[(.*?)\]').findall(s_value)[0]
            iOS['bundleId'] = 'com.btcc.mobiEntStaging'

            device.append(iOS)

        return device



def is_using(port):
    """
    判断端口号是否被占用
    :param port:
    :return:
    """
    cmd = "netstat -an | grep %s" % port

    if os.popen(cmd).readlines():
        return True
    else:
        return False

def get_port(count):
    """
    获得3456端口后一系列free port
    :param count:
    :return:
    """
    port = 3456
    port_list = []
    while True:
        if len(port_list) == count:
            break

        if not is_using(port) and (port not in port_list):
            port_list.append(port)
        else:
            port += 1

    return port_list

def start_server(devices):
    # 进程池
    count = len(devices)
    pool = Pool(processes=count)
    port_list = get_port(count)

    for i in range(count):
        pool.apply_async(run_server, args=(devices[i], port_list[i]))
        time.sleep(3)
        #self.run_server(self.devices[i],port_list[i])

    pool.close()
    pool.join()

class DRIVER:

    driver = None
    OS = None

    @classmethod
    def set_driver(cls, driver):
        cls.driver = driver

    @classmethod
    def set_OS(cls, OS):
        cls.OS = OS

def run_server(device, port):
    r = RunServer(port)
    r.start()

    while not is_running(port):
        time.sleep(1)

    server_url = {
        'hostname': "ununtrium.local",
        'port': port,
    }
    driver = WebDriver(device, server_url)
    driver.init()

    DRIVER.set_driver(driver)
    DRIVER.set_OS(device.get("platformName"))

    run_test(driver)

def run_test(driver):
    """
        运行测试
    """
    test_run(driver, "")

def is_running(port):
        """Determine whether server is running
        :return:True or False
        """
        url = 'http://127.0.0.1:%s/wd/hub/status'
        url1 = url % port
        response = None
        try:
            response = requests.get(url1, timeout=0.01)

            if str(response.status_code).startswith('2'):

                # data = json.loads((response.content).decode("utf-8"))

                # if data.get("staus") == 0:
                return True

            return False
        except requests.exceptions.ConnectionError:
            return False
        except ReadTimeout:
            return False
        finally:
            if response:
                response.close()


class RunServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.cmd = 'macaca server -p %s --verbose' % port

    def run(self):
        os.system(self.cmd)

if __name__ == "__main__":
    b = InitDevice()
    start_server(b.get_device())