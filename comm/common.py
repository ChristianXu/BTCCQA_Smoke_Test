# -*- coding: utf-8 -*-
__author__ = 'sara'

import os
import comm
import yaml
from selenium.common.exceptions import NoSuchElementException
from yaml import Loader, SafeLoader

prjDir = comm.prjDir

config_path = os.path.join(prjDir, "config")


class Info:
    user = None
    website = None
    driver = None
    browser = None

    @classmethod
    def set_info(cls, website, user, d, browser):
        cls.user = user
        cls.website = website
        cls.driver = d
        cls.browser = browser

        comm.Template.set_info(website, browser, user.get("email"))


def get_driver():
    return Info.driver


def get_user():
    return Info.user


def open_url(value):

    Info.driver.get(value)

    is_page_loaded()


def is_page_loaded():
    js = "return document.readyState=='complete'"

    while not Info.driver.execute_script(js):
        sleep(1)


activity = {}
url = {}


def __construct_yaml_str(self, node):
    # Override the default string handling function
    # to always return unicode objects
    return self.construct_scalar(node)
Loader.add_constructor(u'tag:yaml.org,2002:str', __construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', __construct_yaml_str)


def __set_yaml():

    element_path = os.path.join(config_path, Info.website, "element.yaml")
    if len(activity) == 0:

        with open(element_path, encoding='utf8') as f:
            data = yaml.load(f)
            activity.update(data.get("page"))

    url_path = os.path.join(config_path, Info.website, "url.yaml")
    if len(url) == 0:
        with open(url_path, encoding="utf8") as f:
            # f = open(url_path)
            data = yaml.load(f)

            url.update(data.get("url"))


def get_el_dict(page_name, element_name):
    """
    According to the activityName and elementName get element
    :param page_name:
    :param element_name:
    :return:
    """
    __set_yaml()
    element_dict = activity.get(page_name).get(element_name)
    return element_dict


def get_url(url_name):
    __set_yaml()
    return url.get(url_name)


from time import sleep


def get_element(page_name, element_name):

    element_dict = get_el_dict(page_name, element_name)

    path_type = element_dict[0]
    path_value = element_dict[1]

    try:
        if path_type == "id":
            return Info.driver.find_element_by_id(path_value)
        if path_type == "class_name":
            return Info.driver.find_element_by_class_name(path_value)
        if path_type == "xpath":
            return Info.driver.find_element_by_xpath(path_value)
        if path_type == "name":
            return Info.driver.find_element_by_name(path_value)
        if path_type == "tag_name":
            return Info.driver.find_element_by_tag_name(path_value)
        if path_type == "css_selector":
            return Info.driver.find_element_by_css_selector(path_value)
        if path_type == "link_text":
            return Info.driver.find_element_by_link_text(path_value)
        else:
            return None
    except NoSuchElementException:
        return None


def get_elements(page_name, element_name):

    element_dict = get_el_dict(page_name, element_name)

    path_type = element_dict[0]

    path_value = element_dict[1]

    try:
        if path_type == "id":
            return Info.driver.find_elements_by_id(path_value)
        if path_type == "class_name":
            return Info.driver.find_elements_by_class_name(path_value)
        if path_type == "xpath":
            return Info.driver.find_elements_by_xpath(path_value)
        if path_type == "name":
            return Info.driver.find_elements_by_name(path_value)
        if path_type == "tag_name":
            return Info.driver.find_elements_by_tag_name(path_value)
        if path_type == "css_selector":
            return Info.driver.find_elements_by_css_selector(path_value)
        if path_type == "link_text":
            return Info.driver.find_elements_by_link_text(path_value)
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

#
# if __name__ == "__main__":
#
#     __set_yaml()
#     print(get_el_dict("homepage", "login_btn"))
