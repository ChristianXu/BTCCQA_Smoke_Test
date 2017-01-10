__author__ = 'sara'
from comm import common
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


get_element = common.get_element
driver = common.get_driver()


def login(email, password):

    if get_element("homepage", "singIn_btn") is None:
        logout()

    get_element("homepage", "singIn_btn").click()

    get_element("homepage", "email").send_keys(email)
    get_element("homepage", "password").send_keys(password)
    get_element("homepage", "login_btn").click()
    sleep(1)

    while get_element("homepage", "login_loading") is not None:
        sleep(1)


def logout():

    sleep(2)

    e = get_element("homepage", "email_text")
    action = ActionChains(driver)

    action.move_to_element(e).click_and_hold(e).release().perform()

    get_element("homepage", "logout_btn").click()


def get_current_language():

    return get_element("foot", "currentLanguage").text


def switch_language():
    get_element("foot", "currentLanguage").click()
    get_element("foot", "otherLanguage").click()

