import os
import time
import random
import string
import base64
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Your 2Captcha API key
API_KEY = '9a08359dd3706e2bab25751401408f9f'

# Function to solve CAPTCHA using 2Captcha
def solve_captcha(captcha_image_url):
    try:
        # Step 1: Download CAPTCHA image
        captcha_image_data = requests.get(captcha_image_url).content

        # Step 2: Convert image to base64 (2Captcha expects base64-encoded images)
        captcha_image_base64 = base64.b64encode(captcha_image_data).decode('utf-8')

        # Step 3: Send the base64 image to 2Captcha for solving
        url = "http://2captcha.com/in.php"
        response = requests.post(url, data={
            'key': API_KEY,
            'method': 'base64',
            'body': captcha_image_base64,
            'json': 1
        })

        result = response.json()
        print(f"2Captcha initial response: {result}")

        if result['status'] == 1:
            captcha_id = result['request']
            # Step 4: Get the CAPTCHA solution
            solution_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
            
            # Poll for the solution
            max_attempts = 30
            attempts = 0
            
            while attempts < max_attempts:
                solution_response = requests.get(solution_url)
                solution = solution_response.json()
                print(f"Polling attempt {attempts + 1}: {solution}")
                
                if solution['status'] == 1:
                    return solution['request']
                elif solution['request'] == 'CAPCHA_NOT_READY':
                    time.sleep(5)  # Wait before trying again
                    attempts += 1
                else:
                    print(f"Error from 2Captcha: {solution['request']}")
                    return None
            
            print("Max polling attempts reached without solution")
            return None
        else:
            print(f"Failed to submit CAPTCHA to 2Captcha: {result['request']}")
            return None
    except Exception as e:
        print(f"Error in solve_captcha function: {e}")
        return None

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

def main():
    try:
        # Prompt for the Chrome profile directories
        profile_directories = input("Enter the Chrome profile directories (comma-separated): ").split(",")
        profile_directories = [directory.strip() for directory in profile_directories]

        # Create the profile directories if they don't exist
        for directory in profile_directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Read the user agents from the text file
        user_agents_file = r"C:\Users\SeanAlgo\OneDrive\Documents\Dev\Bot\all user agent.txt" 
        try:
            with open(user_agents_file, "r") as file: 
                user_agents = file.read().splitlines()
        except FileNotFoundError:
            print(f"User agents file not found: {user_agents_file}. Using default user agent.")
            user_agents = []

        # Process each profile directory
        for profile_directory in profile_directories:
            try:
                # Generate random identifying information
                mac_address = generate_random_mac_address()
                computer_name = generate_random_computer_name()
                user_agent = random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                
                print(f"\nProcessing profile: {profile_directory}")
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
                
                # Additional arguments to enhance undetectability
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_argument('--disable-web-security')
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)

                # Create WebDriver instance
                chromedriver_path = r"C:\Users\SeanAlgo\OneDrive\Documents\Dev\chromedriver-win64\chromedriver-win64\chromedriver.exe"
                service = Service(executable_path=chromedriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Create wait object with longer timeout
                wait = WebDriverWait(driver, 15)  # Increased timeout to 15 seconds
                
                try:
                    # Set window size
                    driver.set_window_size(500, 800)
                    
                    # Visit website
                    print("Navigating to megapersonals.eu...")
                    driver.get('https://megapersonals.eu/')
                    
                    # Handle terms agreement
                    print("Handling terms agreement...")
                    terms_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.terms-container')))
                    
                    # Scroll through terms
                    last_height = driver.execute_script("return arguments[0].scrollHeight", terms_container)
                    
                    while True:
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", terms_container)
                        time.sleep(0.5)
                        
                        new_height = driver.execute_script("return arguments[0].scrollHeight", terms_container)
                        if new_height == last_height:
                            break
                        last_height = new_height
                    
                    # Check the agreement checkbox
                    checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'checkbox-agree')))
                    driver.execute_script("arguments[0].click();", checkbox)
                    
                    # Submit agreement
                    agree_button = wait.until(EC.element_to_be_clickable((By.ID, 'ageagree')))
                    driver.execute_script("arguments[0].click();", agree_button)
                    
                    # Navigate to login page
                    print("Navigating to login page...")
                    driver.get('https://megapersonals.eu/users/auth/login')
                    
                    # Make sure the page is fully loaded
                    time.sleep(3)
                    
                    # Read credentials from file
                    email_pass_file = r"C:\Users\SeanAlgo\OneDrive\Documents\Dev\Email.txt"
                    with open(email_pass_file, 'r') as file:
                        email_pass = file.read().strip()
                        email, password = email_pass.split(':')
                    
                    # Enter login credentials
                    print("Entering login credentials...")
                    email_input = wait.until(EC.presence_of_element_located((By.ID, 'person_username_field_login')))
                    password_input = wait.until(EC.presence_of_element_located((By.ID, 'person_password_field_login')))
                    
                    email_input.clear()
                    email_input.send_keys(email)
                    
                    password_input.clear()
                    password_input.send_keys(password)
                    
                    # Wait for CAPTCHA to load
                    time.sleep(3)
                    
                    # Handle CAPTCHA
                    print("Handling CAPTCHA...")
                    try:
                        # First, try to find the CAPTCHA using different methods
                        captcha_image = None
                        captcha_image_url = None
                        
                        # Try by ID first
                        try:
                            captcha_image = wait.until(EC.presence_of_element_located((By.ID, 'captcha_image_itself')))
                            captcha_image_url = captcha_image.get_attribute('src')
                            print(f"Found CAPTCHA by ID: {captcha_image_url}")
                        except Exception:
                            print("Could not find CAPTCHA by ID, trying alternative methods...")
                        
                        # If not found by ID, try by CSS selector for img tags
                        if not captcha_image_url:
                            try:
                                # Find all images on the page
                                images = driver.find_elements(By.TAG_NAME, 'img')
                                
                                # Look for an image with 'captcha' in the URL
                                for img in images:
                                    src = img.get_attribute('src')
                                    if src and ('captcha' in src.lower() or 'drome6.com' in src.lower()):
                                        captcha_image = img
                                        captcha_image_url = src
                                        print(f"Found CAPTCHA by scanning images: {captcha_image_url}")
                                        break
                            except Exception as e:
                                print(f"Error trying to find CAPTCHA by scanning images: {e}")
                        
                        # If still not found, take a screenshot to debug
                        if not captcha_image_url:
                            driver.save_screenshot('debug_captcha_page.png')
                            print("Saved screenshot for debugging: debug_captcha_page.png")
                            
                            # Try XPath with contains for partial match on the URL pattern
                            try:
                                captcha_xpath = "//img[contains(@src, 'captcha') or contains(@src, 'drome6.com')]"
                                captcha_image = driver.find_element(By.XPATH, captcha_xpath)
                                captcha_image_url = captcha_image.get_attribute('src')
                                print(f"Found CAPTCHA by XPath: {captcha_image_url}")
                            except Exception:
                                print("Could not find CAPTCHA by XPath method")
                                
                            # Get all page source to check if captcha is in the HTML at all
                            page_source = driver.page_source
                            if 'captcha' in page_source.lower():
                                print("The word 'captcha' was found in the page source")
                                if 'drome6.com' in page_source.lower():
                                    print("The domain 'drome6.com' was found in the page source")
                        
                        if captcha_image_url:
                            print("Solving CAPTCHA...")
                            captcha_solution = solve_captcha(captcha_image_url)
                            
                            if captcha_solution:
                                print(f"CAPTCHA solved: {captcha_solution}")
                                
                                # Try to find captcha input field
                                try:
                                    captcha_input = wait.until(EC.presence_of_element_located((By.ID, 'captcha_code')))
                                except Exception:
                                    # If not found by ID, try alternative selectors
                                    try:
                                        captcha_input = driver.find_element(By.NAME, 'captcha')
                                    except Exception:
                                        # Try by CSS selector for input fields near the captcha image
                                        inputs = driver.find_elements(By.TAG_NAME, 'input')
                                        for inp in inputs:
                                            if 'captcha' in inp.get_attribute('id').lower() or 'captcha' in inp.get_attribute('name').lower():
                                                captcha_input = inp
                                                break
                                
                                if captcha_input:
                                    captcha_input.clear()
                                    captcha_input.send_keys(captcha_solution)
                                    
                                    # Submit login form
                                    print("Submitting login form...")
                                    try:
                                        # Try to find submit button by ID first
                                        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'login_data_submit_button')))
                                    except Exception:
                                        # If not found by ID, try by type attribute
                                        submit_buttons = driver.find_elements(By.XPATH, "//input[@type='submit']")
                                        if submit_buttons:
                                            submit_button = submit_buttons[0]
                                        else:
                                            # Try by button tag
                                            submit_button = driver.find_element(By.TAG_NAME, 'button')
                                    
                                    submit_button.click()
                                    
                                    # Wait for login to complete
                                    time.sleep(5)
                                    print("Login process completed")
                                else:
                                    print("Could not find CAPTCHA input field")
                            else:
                                print("Failed to solve CAPTCHA")
                        else:
                            print("CAPTCHA image URL is missing or invalid")
                    except Exception as e:
                        print(f"Error handling CAPTCHA: {e}")
                    
                    # Wait for user to close browser
                    input("Press Enter to close the browser...")
                    
                except Exception as e:
                    print(f"Error during browser automation: {e}")
                
                finally:
                    # Ensure browser is closed
                    driver.quit()
                    print("Browser closed")
            
            except Exception as e:
                print(f"Error processing profile {profile_directory}: {e}")
    
    except Exception as e:
        print(f"Main function error: {e}")

if __name__ == "__main__":
    main()