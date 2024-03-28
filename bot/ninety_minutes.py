from selenium.webdriver.common.by import By
from time import sleep


class Ninety_minutes(object):
    def __init__(self, driver, url: str) -> None:
        self.driver = driver
        self.url = url
        self.fetch()

    def fetch(self) -> None:
        try:
            d = self.driver
            sleep(1)

            d.get(self.url)
            sleep(3)

            elems = d.find_elements(
                By.CLASS_NAME, "card_1vyetm6-o_O-style_teed7n")
            links = [elem.get_attribute('href') for elem in elems]

            sleep(2)

            elems2 = d.find_elements(By.CLASS_NAME, "wrapper_1fw2qss")
            links.extend([elem.get_attribute('href') for elem in elems2])

            sleep(2)

            elems3 = d.find_elements(By.CLASS_NAME, "wrapper_r90ekb")
            links.extend([elem.get_attribute('href') for elem in elems3])

            print(links)
        except Exception as e:
            print(e)
