import json
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Bot(object):
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-proxy-server")
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options)

    def ninety_minutes(self, url: str):
        try:
            d = self.driver
            sleep(1)
            print("=> Redirecting to", url)
            d.get(url)
            sleep(2)

            elems = d.find_elements(
                By.CLASS_NAME, "card_1vyetm6-o_O-style_teed7n")
            links = [elem.get_attribute('href') for elem in elems]

            sleep(1)

            elems2 = d.find_elements(By.CLASS_NAME, "wrapper_1fw2qss")
            links.extend([elem.get_attribute('href') for elem in elems2])

            sleep(1)

            elems3 = d.find_elements(By.CLASS_NAME, "wrapper_r90ekb")
            links.extend([elem.get_attribute('href') for elem in elems3])

            all_news = []

            for link in links:
                # initialize new dictionary for json
                news = dict()
                print("=> Fetching news from", url)
                d.get(link)
                news["heading"] = d.find_element(
                    By.XPATH, '//h1[@class="tagStyle_mxz06e-o_O-title_dhip6x-o_O-sidesPadding_1kaga1a"]').get_attribute('innerText')
                news["time"] = d.find_element(
                    By.XPATH, '//time[@datetime]').get_attribute('datetime')
                sleep(1)
                image_elem = d.find_element(
                    By.XPATH, '//img[@class="_1emrqjj"]')
                sleep(1)
                # If the image is not in view, scroll to it
                actions = ActionChains(d)
                actions.move_to_element(image_elem).perform()

                # Wait until the image is in view
                WebDriverWait(d, 10).until(EC.visibility_of(image_elem))

                # Extracting image source
                image_src = image_elem.get_attribute('src')

                # Splitting the image link at the unwanted parameters and retaining the rest of the URL
                parts = image_src.split("/")

                # Find the indices of "upload/" and "/images"
                upload_index = parts.index("upload")
                images_index = parts.index("images")
                new_url_parts = parts[:upload_index + 1] + parts[images_index:]

                # Reconstructing the cleaned image link
                cleaned_image_link = "/".join(new_url_parts)
                news["image"] = cleaned_image_link
                # Initialize an empty string to store the concatenated content
                sleep(1)
                content = ""
                # Iterate through each element and concatenate its text content
                for elem in d.find_elements(By.XPATH, '//p[@class="tagStyle_z4kqwb-o_O-style_1tcxgp3-o_O-style_1pinbx1-o_O-style_48hmcm"]'):
                    content += elem.get_attribute("innerText") + " "

                # Assign the concatenated content to the news dictionary
                # Remove leading and trailing whitespace
                news["content"] = content.strip()
                news["link"] = link
                all_news.append(news)

                # Sleep to avoid overloading the website
                sleep(5)

            # Write all_news to a JSON file
            directory = os.path.join(os.getcwd(), 'data')
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, 'news.json')
            with open(path, 'w') as f:
                json.dump(all_news, f, indent=4)

            print("All news saved to news.json")

        except NoSuchElementException as e:
            pass
        except Exception as e:
            print(e)
