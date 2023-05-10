from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
from selenium.webdriver.remote.file_detector import LocalFileDetector

"""
    example image_url_tuples = [
        "FCB Barcelona",
        (
            "https://iicanada.org/system/files/webform/306686-player10-headshot.jpg",
            "https://iicanada.org/system/files/webform/306686-player10-govId.jpg",
            "hassani zamanuddin",
            "03/19/1986"
        )
    ]
"""
def download_images(image_url_tuples):
    team_name = image_url_tuples[0]
    team_category = image_url_tuples[1]
    image_url_tuples = image_url_tuples[2:]

    username = os.environ.get('IICANADA_USERNAME')
    password = os.environ.get('IICANADA_PASSWORD')

    # Create a Chrome webdriver instance
    chrome_service = ChromeService(executable_path='/usr/local/bin/chromedriver')
    chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without displaying the GUI
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Navigate to the website
    driver.get("https://iicanada.org")

    # Click the "Login" button
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Login')]")))
    login_button.click()

    # Enter login credentials
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='edit-name']")))
    password_field = driver.find_element(By.XPATH, "//input[@id='edit-pass']")
    username_field.send_keys(username)
    password_field.send_keys(password)

    time.sleep(15)

    for i, image_url_tuple in enumerate(image_url_tuples):
        headshot = image_url_tuple[0]
        govt_id = image_url_tuple[1]
        full_name = image_url_tuple[2]
        dob = image_url_tuple[3]

        if not os.path.exists(team_name):
            os.makedirs(team_name)

        if not os.path.exists(f"{team_name}-{category}/data"):
            os.makedirs(f"{team_name}-{category}/data")

        folder_path = f"{team_name}-{category}/data/{str(i)}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(f"{folder_path}/info.txt", 'w') as file:
            file.write(full_name)
            file.write('\n')
            file.write(dob)


        for j, image_url in enumerate([headshot, govt_id]):
            # Send a keyboard shortcut to open a new tab
            action_chains = ActionChains(driver)
            action_chains.key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            driver.get(image_url)

            image_prefix = 'headshot' if j == 0 else 'id'
            driver.save_screenshot(f"{team_name}/data/{i}/{image_prefix}.jpg")