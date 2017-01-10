__author__ = 'sara'

from comm import common
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
driver = common.get_driver()
get_element = common.get_element
get_elements = common.get_elements


def login(email, password):

    try:

        get_element("exchange", "sign_in_btn").click()
    except NoSuchElementException:
        logout()
        get_element("exchange", "sign_in_btn").click()

    get_element("exchange", "email").send_keys(email)
    get_element("exchange", "password").send_keys(password)

    get_element("exchange", "login_btn").click()

    e = get_element("exchange", "login_btn_loading")

    while e.get_attribute("style") == "display: none;":
        sleep(1)

    sleep(2)


def logout():

    e = get_element("exchange", "email_text")
    action = ActionChains(driver)

    action.move_to_element(e).click_and_hold(e).release().perform()

    sleep(1)

    get_element("exchange", "logout_btn").click()

    sleep(1)

