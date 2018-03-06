import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


browsers = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome
}

self = sys.modules[__name__]
self.browser = None
self.wait = None


def init(browser, url, wait=10, maximize=True, language=None):
    """Initialise a selenium controlled browser session

    Parameters
    ----------
    browser : str
        to indicate the desired browser. Must be a key in the browsers dict
    url : str
        the initial url which the browser should open
    wait : int
        default wait time in seconds
    maximize : bool
        whether the browser window should be maximized
    language : str
        a standard language definition string (e.g. 'en_GB') for use with
        Chrome
    """
    kwargs = {}
    if browser == 'chrome' and language is not None:
        options = webdriver.ChromeOptions()
        options.add_argument(f'--lang={language}')
        kwargs['chrome_options'] = options
    self.browser = browsers[browser](**kwargs)
    self.wait = WebDriverWait(self.browser, wait)
    if maximize:
        self.browser.maximize_window()
    self.browser.get(url)


def _select_by(select_by=None):
    if not select_by:
        return By.XPATH
    else:
        return getattr(By, select_by.upper())


def click(locator, delay=None, select_by=None):
    """Click the specified element

    Parameters
    ----------
    locator : str
        xpath, class name or id
    delay : int
        time in seconds to wait after clicking
    select_by : str
        representing a valid selenium By selector (e.g. 'id').
    """
    select_by = _select_by(select_by)
    self.wait.until(ec.element_to_be_clickable((select_by, locator))).click()

    if delay is not None:
        time.sleep(delay)


def send_keys(
    locator, keys, clear=False, pause=None, delay=None, select_by=None
):
    """Send keys to selected element

    Parameters
    ----------
    locator : str
        xpath, class name or id
    keys : str
        the keys to be sent
    clear : bool
        whether to clear the element before sending keys
    pause : int
        time in seconds to pause between clearing and sending keys
    delay : int
        time in seconds to wait after sending all keys
    select_by : str
        representing a valid selenium By selector (e.g. 'id').
    """
    select_by = _select_by(select_by)
    element = self.wait.until(
        ec.presence_of_element_located((select_by, locator)))
    if clear:
        element.clear()

    if pause is None:
        element.send_keys(keys, Keys.TAB)
    else:
        element.send_keys(keys)
        time.sleep(pause)
        element.send_keys(Keys.TAB)

    if delay is not None:
        time.sleep(delay)


def get_text(locator, select_by=None):
    """Return the text value of the selected element

    Parameters
    ----------
    locator : str
        xpath, class name or id
    select_by : str
        representing a valid selenium By selector (e.g. 'id').
    """
    select_by = _select_by(select_by)
    text = self.wait.until(
        ec.presence_of_element_located((select_by, locator))).text
    return text


def login(email, password):
    """Login to a standard anvil login form

    Parameters
    ----------
    email : str
        the email address to use
    password : str
        the password to use
    """
    main_xpath = '/html/body/div[4]/div/div'
    email_xpath = f'{main_xpath}/div[2]/div/ul/li[2]/input'
    password_xpath = f'{main_xpath}/div[2]/div/ul/li[4]/input'
    login_xpath = f'{main_xpath}/div[3]/button[1]'

    send_keys(email_xpath, email)
    send_keys(password_xpath, password)
    click(login_xpath)


def signup(email, password):
    main_xpath = '/html/body/div[4]/div/div'
    signup_xpath = f'{main_xpath}/div[2]/div/ul/li[7]/a'
    click(signup_xpath, delay=1)

    email_xpath = f'{main_xpath}/div[2]/div/ul/li[2]/input'
    password_1_xpath = f'{main_xpath}/div[2]/div/ul/li[4]/input'
    password_2_xpath = f'{main_xpath}/div[2]/div/ul/li[6]/input'
    signup_xpath = f'{main_xpath}/div[3]/button[1]'

    send_keys(email_xpath, email)
    send_keys(password_1_xpath, password)
    send_keys(password_2_xpath, password)
    click(signup_xpath)
