# =============================================================================
# browser.py
# Selenium driver setup and low-level DOM helpers.
# Nothing in here knows about Scoresway's page structure — it's purely generic.
# =============================================================================

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

import config


def get_driver(url: str) -> webdriver.Chrome:
    """
    Launch a Chrome driver, navigate to url, and wait for the page to settle.
    Returns the ready driver.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(config.DRIVER_IMPLICIT_WAIT)
    sleep(config.DRIVER_LOAD_SLEEP)
    return driver


def remove_cookie_dialog(driver: webdriver.Chrome) -> None:
    """
    Remove OneTrust cookie banners and any other common consent overlays
    that can intercept clicks. Safe to call multiple times.
    """
    driver.execute_script("""
        var ids = ['onetrust-banner-sdk', 'onetrust-consent-sdk', 'onetrust-pc-sdk'];
        ids.forEach(function(id) {
            var el = document.getElementById(id);
            if (el) el.remove();
        });
        document.querySelectorAll(
            '[class*="cookie"], [class*="consent"], [class*="gdpr"], [id*="cookie"]'
        ).forEach(function(el) { el.remove(); });
    """)


def js_click(driver: webdriver.Chrome, element) -> None:
    """
    Scroll element to the centre of the viewport and click via JavaScript.
    This bypasses any overlay/intercept that would block a native .click().
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    sleep(0.5)
    driver.execute_script("arguments[0].click();", element)


def wait_for(driver: webdriver.Chrome, css_selector: str, timeout: int = None):
    """
    Wait until an element matching css_selector is present in the DOM.
    Returns the element. Uses config.EXPLICIT_WAIT_TIMEOUT if timeout not given.
    """
    t = timeout if timeout is not None else config.EXPLICIT_WAIT_TIMEOUT
    return WebDriverWait(driver, t).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )
