**Doctor Information Scraper**

**Overview**

This Python script automates the extraction of doctor information from the Andalusia Health website and an external API. It gathers details such as names, profile URLs, phone numbers, addresses, ratings, and more. The extracted data is stored in MongoDB Atlas and exported to CSV and JSON formats. The script also performs data analysis to provide insights into the extracted doctors' data.

Features

Uses Selenium to navigate and scrape service categories from the Andalusia Health website.

Sends API requests to fetch doctor details based on services.

Stores extracted data in MongoDB Atlas.

Analyzes the dataset to count total doctors, identify duplicate phone numbers, and check doctors with multiple locations.

Exports data and analysis results to CSV and JSON files.

Prerequisites

Ensure you have the following installed:

Python 3.x

Google Chrome (latest version)

MongoDB Atlas (configured cluster)

Required Python Packages

Install the dependencies using:

pip install selenium requests pandas pymongo

Setup and Execution

MongoDB Atlas Configuration

Replace mongodb+srv://gunjan1:Gl428EJ4wYGraULW@cluster0.um2n0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 with your MongoDB Atlas connection string.

Run the script

python script.py

Data Extraction Process

The script initializes a Selenium WebDriver to access https://www.andalusiahealth.com/.

It navigates to the "Services" section and extracts service names.

API calls are made to retrieve doctors based on extracted services.

Doctor details are stored in MongoDB Atlas and processed for analysis.

The data is exported to doctors_data.csv and doctors_data.json.

An analysis report is generated as analysis_report.json.

Data Analysis

The script performs the following analysis:

Total Number of Doctors: Count of all extracted doctor records.

Doctors with Ratings: Count of doctors having a rating greater than 0.

Duplicate Phone Numbers: Identifies doctors sharing the same phone number.

Doctors with Multiple Locations: Identifies doctors listed in more than one location.

**Output Files**

**doctors_data.csv** - Extracted doctor data in CSV format.

**doctors_data.json** - Extracted doctor data in JSON format.

**analysis_report.json** - JSON report containing summary statistics.
**Notes**

Ensure ChromeDriver is compatible with your Chrome version.

The script includes sleep delays to handle dynamic content loading.

If facing MongoDB connection issues, verify the cluster settings and IP whitelisting.

License

This project is for educational purposes. Feel free to modify and use it as needed.
