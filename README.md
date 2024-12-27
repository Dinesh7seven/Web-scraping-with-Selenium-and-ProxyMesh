# Web-scraping-with-Selenium-and-ProxyMesh

Steps to Implement
1. Selenium Script to Fetch Twitter Trends
Automate login to Twitter.
Scrape the top 5 trending topics from the "What’s Happening" section.
Use ProxyMesh to change the IP address for each request.
2. MongoDB Storage
Install MongoDB locally or use a cloud-based MongoDB (e.g., MongoDB Atlas).
Create a unique ID for each run of the script.
Save data fields as specified.
3. HTML Interface
Create an HTML page with a button to trigger the Selenium script.
Display the results dynamically after the script runs.
Show a JSON extract of the MongoDB record.
4. Integration
Use Flask (or Django) to connect the backend (Python script + MongoDB) with the front-end (HTML page).


 Let’s start by automating the login and fetching the trending topics using Selenium.

Step 1: Set Up the Environment
-> Install the necessary libraries:
           - pip install selenium pymongo flask dnspython
           
Step 2: Selenium Script to Log in and Fetch Trends
Here’s a Python script for logging into Twitter and extracting the top 5 trends:

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

Step 3: Create the HTML Page
Here’s the HTML template with a button to trigger the Selenium script:

            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Twitter Trends</title>
            </head>
            <body>
                <h1>Twitter Trending Topics</h1>
                <button id="run-script">Click here to run the script</button>
                <div id="results"></div>
            
                <script>
                    document.getElementById("run-script").onclick = async function () {
                        const response = await fetch("/run-script", { method: "POST" });
                        const data = await response.json();
            
                        const resultDiv = document.getElementById("results");
                        resultDiv.innerHTML = `
                            <p>These are the most happening topics as on ${data.end_time}:</p>
                            <ul>
                                <li>${data.trend1}</li>
                                <li>${data.trend2}</li>
                                <li>${data.trend3}</li>
                                <li>${data.trend4}</li>
                                <li>${data.trend5}</li>
                            </ul>
                            <p>The IP address used for this query was ${data.ip_address}.</p>
                            <p>Here’s a JSON extract of this record from MongoDB:</p>
                            <pre>${JSON.stringify(data, null, 2)}</pre>
                            <button onclick="window.location.reload()">Click here to run the query again</button>
                        `;
                    };
                </script>
            </body>
            </html>

Step 4: Backend with Flask
Here’s the Flask application to handle the Selenium script and serve the HTML:
          from flask import Flask, jsonify, render_template, request
          from pymongo import MongoClient
          import subprocess
          
          app = Flask(__name__)
          
          # MongoDB connection
          client = MongoClient("mongodb://localhost:27017/")
          db = client['twitter_trends']
          collection = db['trends']
          
          @app.route("/")
          def home():
              return render_template("index.html")
          
          @app.route("/run-script", methods=["POST"])
          def run_script():
              # Trigger the Selenium script
              subprocess.run(["python", "selenium_script.py"])  # Replace with the correct script path
          
              # Fetch the latest record from MongoDB
              latest_record = collection.find_one(sort=[("_id", -1)])
              return jsonify(latest_record)
          
          if __name__ == "__main__":
              app.run(debug=True)

Step 5: Set Up File Structure
Organize your project like this:

           project/
          │ 
          ├── templates/
          │   └── index.html
          ├── selenium_script.py
          ├── app.py
          └── requirements.txt


Next Steps : 
1.Save the HTML code in the templates/index.html file.
2.Run the Flask application with:
      python app.py
3.Open your browser and visit http://127.0.0.1:5000.
4.Click the button to run the Selenium script and view the results.
