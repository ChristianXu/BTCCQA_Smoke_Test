# -*- coding: utf-8 -*-
__author__ = 'sara'

import configparser
import codecs
import os
import comm
import yaml
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

prjDir = comm.prjDir

configfile_path = os.path.join(prjDir, "config", "setting.ini")
geckodriver_path = os.path.join(prjDir, "config", "geckodriver")
chrome_path = os.path.join(prjDir, "config", "chromedriver")
element_path = os.path.join(prjDir, "config", "btcchina", "element.yaml")
url_path = os.path.join(prjDir, "config", "btcchina", "url.yaml")


class ReadConfig:

    cf = None

    @classmethod
    def get_value(cls, section, name):

        if cls.cf is None:
            fd = open(configfile_path)
            data = fd.read()
            # remove BOM
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                file = codecs.open(configfile_path, "w")
                file.write(data)
                file.close()
            fd.close()

            cls.cf = configparser.ConfigParser()
            cls.cf.read(configfile_path)

        return cls.cf.get(section, name)


# def get_url(url_name):
#     website = "%s_url" % ReadConfig.get_value("system", "website")
#
#     return ReadConfig.get_value(website, url_name)


class DRIVER:

    driver = None

    @classmethod
    def get_driver(cls):

        if DRIVER.driver is None:
            DRIVER.driver = webdriver.Chrome(executable_path=chrome_path)
            DRIVER.driver.maximize_window()
            DRIVER.driver.set_page_load_timeout(120)
            DRIVER.driver.implicitly_wait(10)

        return DRIVER.driver


def get_driver():
    return DRIVER.get_driver()


def open_url(url):

    DRIVER.driver.get(url)

    is_page_loaded()


def is_page_loaded():
    js = "return document.readyState=='complete'"

    while not DRIVER.driver.execute_script(js):
        sleep(1)


activity = {}
url = {}
from xml.etree import ElementTree as elementTree


def set_xml():
    """
    get the xml file's value
    :use:
    a = getXml(path)

    print(a.get(".module.GuideActivity").get("skip").get("type"))
    :param: xmlPath
    :return:activity
    """
    if len(activity) == 0:

        xml_path = os.path.join(prjDir, "config", "element.xml")
        # open the xml file
        per = elementTree.parse(xml_path)
        all_element = per.findall('web_page')

        for firstElement in all_element:
            activity_name = firstElement.get("name")

            element = {}

            for secondElement in firstElement.getchildren():
                element_name = secondElement.get("name")

                element_child = {}
                for thirdElement in secondElement.getchildren():

                    element_child[thirdElement.tag] = thirdElement.text

                element[element_name] = element_child
            activity[activity_name] = element


def set_yaml():
    if len(activity) == 0:
        f = open(element_path)
        data = yaml.load(f)

        activity.update(data.get("page"))

    if len(url) == 0:
        f = open(url_path)
        data = yaml.load(f)

        url.update(data.get("url"))


def get_el_dict(page_name, element_name):
    """
    According to the activityName and elementName get element
    :param page_name:
    :param element_name:
    :return:
    """
    # set_xml()
    set_yaml()
    element_dict = activity.get(page_name).get(element_name)
    return element_dict


def get_url(url_name):
    set_yaml()
    return url.get(url_name)


from time import sleep


driver = get_driver()


def get_element(page_name, element_name):

    element_dict = get_el_dict(page_name, element_name)
    # path_type = element_dict.get("pathtype")
    # path_value = element_dict.get("pathvalue")

    path_type = element_dict[0]
    path_value = element_dict[1]

    try:
        if path_type == "id":
            return driver.find_element_by_id(path_value)
        if path_type == "class_name":
            return driver.find_element_by_class_name(path_value)
        if path_type == "xpath":
            return driver.find_element_by_xpath(path_value)
        if path_type == "name":
            return driver.find_element_by_name(path_value)
        if path_type == "tag_name":
            return driver.find_element_by_tag_name(path_value)
        if path_type == "css_selector":
            return driver.find_element_by_css_selector(path_value)
        if path_type == "link_text":
            return driver.find_element_by_link_text(path_value)
        else:
            return None
    except NoSuchElementException:
        return None


def get_elements(page_name, element_name):

    element_dict = get_el_dict(page_name, element_name)
    # path_type = element_dict.get("pathtype")
    # path_value = element_dict.get("pathvalue")

    path_type = element_dict[0]
    path_value = element_dict[1]

    try:
        if path_type == "id":
            return driver.find_elements_by_id(path_value)
        if path_type == "class_name":
            return driver.find_elements_by_class_name(path_value)
        if path_type == "xpath":
            return driver.find_elements_by_xpath(path_value)
        if path_type == "name":
            return driver.find_elements_by_name(path_value)
        if path_type == "tag_name":
            return driver.find_elements_by_tag_name(path_value)
        if path_type == "css_selector":
            return driver.find_elements_by_css_selector(path_value)
        if path_type == "link_text":
            return driver.find_elements_by_link_text(path_value)
        else:
            return None
    except NoSuchElementException:
        return None

import contextlib


@contextlib.contextmanager
def my_assert(msg):
    try:
        yield
        comm.Template.add_result(msg, "OK", "")
    except AssertionError as ex:
        print(ex)
        comm.Template.add_result(msg, "NG", ex)

