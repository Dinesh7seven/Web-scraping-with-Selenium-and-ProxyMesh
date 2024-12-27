from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pymongo import MongoClient
import uuid
import time
import datetime

# Set up ProxyMesh (Replace USERNAME and PASSWORD)
PROXY = "http://USERNAME:PASSWORD@us-west.proxymesh.com:31280"

# Configure Selenium with ProxyMesh
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = PROXY
proxy.ssl_proxy = PROXY

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
options.add_argument('--disable-extensions')  # Disable extensions

service = Service("path_to_chromedriver")
capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)
driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Adjust for your MongoDB connection
db = client['twitter_trends']
collection = db['trends']

try:
    # Step 1: Log in to Twitter
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 10)
    
    # Enter username
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.send_keys("your_username")  # Replace with your Twitter username
    username_input.send_keys(Keys.RETURN)

    # Wait for password input
    time.sleep(2)
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys("your_password")  # Replace with your Twitter password
    password_input.send_keys(Keys.RETURN)

    # Step 2: Navigate to home page and fetch trending topics
    time.sleep(5)  # Wait for the homepage to load
    trends_section = wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(., 'What’s happening')]")))
    trends = trends_section.find_elements(By.XPATH, ".//span[contains(@class, 'css-901oao')][1:5]")
    trend_names = [trend.text for trend in trends[:5]]  # Get top 5 trends

    # Step 3: Store data in MongoDB
    run_id = str(uuid.uuid4())
    current_ip = driver.execute_script("return window.navigator.connection.effectiveType")  # Replace with Proxy IP fetch logic if needed
    record = {
        "_id": run_id,
        "trend1": trend_names[0] if len(trend_names) > 0 else None,
        "trend2": trend_names[1] if len(trend_names) > 1 else None,
        "trend3": trend_names[2] if len(trend_names) > 2 else None,
        "trend4": trend_names[3] if len(trend_names) > 3 else None,
        "trend5": trend_names[4] if len(trend_names) > 4 else None,
        "end_time": datetime.datetime.now(),
        "ip_address": current_ip
    }
    collection.insert_one(record)
    print("Data stored in MongoDB:", record)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    driver.quit()