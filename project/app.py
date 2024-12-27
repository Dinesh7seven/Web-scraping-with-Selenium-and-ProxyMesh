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