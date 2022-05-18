from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.conf import settings
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

try:
    web_driver_module = settings.SELENIUM_WEBDRIVER
except AttributeError:
    from selenium.webdriver.firefox import webdriver as web_driver_module


class CustomWebDriver(web_driver_module.WebDriver):
    """Our own WebDriver with some helpers added"""

    def find_css(self, css_selector):
        """Shortcut to find elements by CSS. Returns either a list or singleton"""
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=7):
        """ Shortcut for WebDriverWait"""
        try:
            return WebDriverWait(self, timeout).until(lambda driver : driver.find_css(css_selector))
        except:
            self.quit()

# Create your tests here.
class EventFormTest(LiveServerTestCase):

  def test_api_form(self):
    selenium = webdriver.Chrome()
    selenium.get('http://127.0.0.1:8000/api/events')
    event_drink_img_val = selenium.find_element_by_id('picamera_img_val')
    event_drink_ocr_text = selenium.find_element_by_id('ocr_text')
    event_glass_weight = selenium.find_element_by_id('weight')
    event_barkeeping_score = selenium.find_element_by_id('score')
    submit = selenium.find_element_by_css_selector('btn btn-primary js-tooltip')

    event_drink_img_val.send_keys('[1,2,3],[1,2,3],[1,2,3]')
    event_drink_ocr_text.send_keys('Pina Colada')
    event_glass_weight.send_keys(78.99)
    event_barkeeping_score.send_keys(True)

    submit.send_keys(Keys.RETURN)

    #check result; page source looks at entire html document
    assert 'Pina Colada' in selenium.page_source