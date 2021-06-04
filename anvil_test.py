"""A module to facilitate automated testing of Anvil apps using selenium"""
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Test project team members listed at
# https://github.com/anvilistas/anvil-test/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-test

import time
from typing import Optional, Union

import attr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

__version__ = "0.0.2"
_browsers = {"firefox": webdriver.Firefox, "chrome": webdriver.Chrome}


def _select_by(select_by=None):
    return getattr(By, select_by.upper()) or By.XPATH


@attr.s(auto_attribs=True)
class Session:
    browser: Union[webdriver.Chrome, webdriver.Firefox]
    wait: WebDriverWait

    def maximize_window(self):
        self.browser.maximize_window()

    def navigate_to(self, url):
        self.browser.get(url)

    def click(self, locator, delay=None, select_by=None):
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
        select_by = self._select_by(select_by)
        self.wait.until(ec.element_to_be_clickable((select_by, locator))).click()

        if delay is not None:
            time.sleep(delay)

    def send_keys(
        self, locator, keys, clear=False, pause=None, delay=None, select_by=None
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
        element = self.wait.until(ec.presence_of_element_located((select_by, locator)))
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

    def get_text(self, locator, select_by=None):
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
            ec.presence_of_element_located((select_by, locator))
        ).text
        return text

    def login(self, email, password):
        """Login to a standard anvil login form

        Parameters
        ----------
        email : str
            the email address to use
        password : str
            the password to use
        """
        main_xpath = "/html/body/div[4]/div/div"
        email_xpath = f"{main_xpath}/div[2]/div/ul/li[2]/input"
        password_xpath = f"{main_xpath}/div[2]/div/ul/li[4]/input"
        login_xpath = f"{main_xpath}/div[3]/button[1]"

        self.send_keys(email_xpath, email)
        self.send_keys(password_xpath, password)
        self.click(login_xpath)

    def signup(self, email, password):
        main_xpath = "/html/body/div[4]/div/div"
        signup_xpath = f"{main_xpath}/div[2]/div/ul/li[7]/a"
        self.click(signup_xpath, delay=1)

        email_xpath = f"{main_xpath}/div[2]/div/ul/li[2]/input"
        password_1_xpath = f"{main_xpath}/div[2]/div/ul/li[4]/input"
        password_2_xpath = f"{main_xpath}/div[2]/div/ul/li[6]/input"
        signup_xpath = f"{main_xpath}/div[3]/button[1]"

        self.send_keys(email_xpath, email)
        self.send_keys(password_1_xpath, password)
        self.send_keys(password_2_xpath, password)
        self.click(signup_xpath)


def new_session(browser: str, wait: int, language: Optional[str] = None) -> Session:
    kwargs = dict()
    if browser == "chrome" and language is not None:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--lang={language}")
        kwargs["chrome_options"] = options
    _browser = _browsers[browser](**kwargs)
    _wait = WebDriverWait(_browser, wait)
    return Session(_browser, _wait)
