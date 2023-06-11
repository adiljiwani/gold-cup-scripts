from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from selenium.webdriver.common.action_chains import ActionChains
import os

base_folder = "2023"


class Player:
    def __init__(self, full_name: str, dob: str, email_address: str, headshot: str, govt_id: str):
        self.full_name = full_name
        self.dob = dob
        self.email_address = email_address
        self.headshot = headshot
        self.govt_id = govt_id


class Team:
    def __init__(self, name: str, category: str, players: list[Player]):
        self.name = name
        self.category = category
        self.players = players


def download_images(teams: list[Team]):
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
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Login')]")))
    login_button.click()

    # Enter login credentials
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='edit-name']")))
    password_field = driver.find_element(By.XPATH, "//input[@id='edit-pass']")
    username_field.send_keys(username)
    password_field.send_keys(password)

    time.sleep(15)

    for team in teams:
        if not os.path.exists(team.name):
            os.makedirs(team.name)

        data_path = f"{base_folder}/{team.name}-{team.category}/data"
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        else:
            # Don't download team info if we already have it downloaded
            continue

        for i, player in enumerate(team.players):
            folder_path = f"{data_path}/{str(i)}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(f"{folder_path}/info.txt", 'w') as file:
                file.write(player.full_name)
                file.write('\n')
                file.write(player.dob)

            for j, image_url in enumerate([player.headshot, player.govt_id]):
                if player.headshot == '' or player.govt_id == '':
                    continue
                # Send a keyboard shortcut to open a new tab
                action_chains = ActionChains(driver)
                action_chains.key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()

                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[-1])

                driver.get(image_url)

                time.sleep(1)
                image_prefix = 'headshot' if j == 0 else 'id'
                driver.save_screenshot(f"{data_path}/{i}/{image_prefix}.jpg")
