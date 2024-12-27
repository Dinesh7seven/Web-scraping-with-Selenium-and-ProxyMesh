Setup Instructions
1. Clone the Repository
       git clone https://github.com/yourusername/twitter-trends-scraper.git
       cd twitter-trends-scraper
2. Configure Selenium
  - Download ChromeDriver from here.
  - Place the executable in your PATH or specify its location in selenium_script.py.
3. Configure ProxyMesh
  - Replace USERNAME and PASSWORD in selenium_script.py with your ProxyMesh credentials.
4. Configure Twitter Login
  - Update the your_username and your_password placeholders in selenium_script.py with your Twitter credentials.
5. Set Up MongoDB
  - Install MongoDB locally or use a cloud-based MongoDB like MongoDB Atlas.
  - Adjust the connection URI in both selenium_script.py and app.py.
6. Run the Application
 - Start the Flask application:
        python app.py
 - Open your browser and visit http://127.0.0.1:5000.

