import requests
import random
import string
import signal
import os
import time 
import time
import random
import string
import signal
import os
import time
import winsound
from datetime import datetime
from selenium import webdriver
import pytz
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver



# Rest of the code...

# Generate a random MAC address
def generate_random_mac_address():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Generate a random computer name
def generate_random_computer_name(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))






# Prompt for the Chrome profile directories
profile_directories = input("Enter the Chrome profile directories (comma-separated): ").split(",")

# Create the profile directories if they don't exist
for directory in profile_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Read the user agents from the text file
user_agents_file = r"C:\Users\SeanAlgo\OneDrive\Documents\Dev\Bot\all user agent.txt" 
with open(user_agents_file, "r") as file: 
    user_agents = file.read().splitlines()

# Rest of the code...
for profile_directory in profile_directories:
    # Print the generated MAC address, computer name, and user agent
    mac_address = generate_random_mac_address()
    computer_name = generate_random_computer_name()
    user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    print("Generated MAC address:", mac_address)
    print("Generated computer name:", computer_name)
    print("Selected user agent:", user_agent)

 

       # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f'--user-data-dir={profile_directory}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-webrtc')
    chrome_options.add_argument('--disable-features=WebRtcHideLocalIpsWithMdns')
    chrome_options.add_argument('--disable-features=WebRtcLocalIpsWithMdns')


    chrome_options.add_argument(f'--user-agent={user_agent}')
    chrome_options.add_argument('--window-size=375,812')  # Adjust the width and height as needed
    chrome_options.add_argument('--window-position=0,0')  # Set the window position to top left

            # Additional arguments to enhance undetectability
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])




    
       # Replace this line with your chromedriver path 
    chromedriver_path = r"C:\Users\SeanAlgo\OneDrive\Documents\Dev\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Provide the correct path

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Maximize the window
    driver.maximize_window()

        # Set the browser window size to a specific width and height (adjust as needed)
    driver.set_window_size(500, 800)
    # Use the driver to browse the website
    driver.get('https://megapersonals.eu/')

    
# Find the scrollable terms container element
terms_container = driver.find_element(By.CSS_SELECTOR, '.terms-container')

# Start scrolling until we reach the bottom
last_height = driver.execute_script("return arguments[0].scrollHeight", terms_container)

while True:
    # Scroll down a little bit
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", terms_container)
    time.sleep(1)  # Adjust sleep time for performance

    # Check if we've scrolled to the bottom
    new_height = driver.execute_script("return arguments[0].scrollHeight", terms_container)
    if new_height == last_height:
        break  # Exit loop if we've reached the bottom
    last_height = new_height

# Once the scrolling is complete, check the checkbox
checkbox = driver.find_element(By.ID, 'checkbox-agree')
driver.execute_script("arguments[0].click();", checkbox)

# Wait for the checkbox interaction to update the UI (optional)
time.sleep(2)

# Submit the form after agreeing
agree_button = driver.find_element(By.ID, 'ageagree')
driver.execute_script("arguments[0].click();", agree_button)

# Wait for the form submission to complete (optional)
time.sleep(2)







    # Wait for user action before closing the browser
input("Press Enter to close the browser...")
driver.quit()
