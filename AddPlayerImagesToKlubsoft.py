

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

username = "adiljiwani@gmail.com"
password = "B!smillah5"

# Create a Chrome webdriver instance
chrome_service = ChromeService(executable_path='/usr/local/bin/chromedriver')
chrome_options = ChromeOptions()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without displaying the GUI
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navigate to the website
driver.get("https://dev.klubsoft.com/en/o/U2FsdGVkX1bFbFbMgif1OwvbmOsFRM0FeVCjDLjJFSpQtgbKT2lbFbFbWSRzRdQleXq9bFbFbc1q/tournaments/U2FsdGVkX1aFaFaXqH13NfJoj4jgf6TMMYreUzbFbFb4d3xHnoB02T3zjs7pjOo7wCMAJaFaFarl/feeds")

# Click the "Login" button
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='@@header-btn-login']")))
login_button.click()

# # Enter login credentials
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='signIn_inputEmail']")))
password_field = driver.find_element(By.XPATH, "//input[@id='signIn_inputPassword']")
username_field.send_keys(username)
password_field.send_keys(password)

# login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='signIn_btn_login']")))
# login_button.click()

# Press Enter to submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the modal dialog to disappear
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'myModal')))

# participants_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Participants')))
# participants_tab.click()
participants_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-link-id1']")))
participants_tab.click()

view_and_finalize_participants_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn btn-round btn-outline-alter-warning pull-right ng-tns-c240-6 ng-star-inserted")))
view_and_finalize_participants_button.click()

# # Close the webdriver
# driver.quit()

# def download_image(url, file_path):
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#         with open(file_path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         print(f"Image downloaded successfully to: {file_path}")
#     except requests.exceptions.HTTPError as errh:
#         print("HTTP Error:", errh)
#     except requests.exceptions.ConnectionError as errc:
#         print("Error connecting:", errc)
#     except requests.exceptions.Timeout as errt:
#         print("Timeout Error:", errt)
#     except requests.exceptions.RequestException as err:
#         print("Error:", err)

# import requests

# headshot_file_path = 'headshot.jpg'

# download_image('https://iicanada.org/system/files/webform/306686-player1-headshot.jpg', headshot_file_path)