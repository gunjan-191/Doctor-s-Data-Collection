from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests, json
import pandas as pd
from pymongo import MongoClient

# Initialize MongoDB Atlas Connection
client = MongoClient("mongodb+srv://gunjan1:Gl428EJ4wYGraULW@cluster0.um2n0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["DoctorsDatabase"]  # Database Name
collection = db["Doctors"]  # Collection Name

# Initialize WebDriver
driver = webdriver.Chrome()

# Open website
url = "https://www.andalusiahealth.com/"
driver.get(url)
time.sleep(5)  # Wait for page to load

# Locate the "Services" tab
services_tab = driver.find_element(By.XPATH, "//a[contains(text(), 'Services')]")

# Hover to reveal dropdown menu
actions = ActionChains(driver)
actions.move_to_element(services_tab).perform()
time.sleep(3)

# Extract service names
dropdown_items = driver.find_elements(By.XPATH, '//div[@class="dropDown"]//div[@class="dropdown-list service-list"]/a')
services = [item.text for item in dropdown_items if item.text.strip()]

# Close the browser after extraction
driver.quit()

doctors = []

for service in services:
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }   

    params = {
        'searchText': service,
        'disabledEmployedRankings': 'false',
    }

    # API call to fetch doctor details
    response = requests.get(
        'https://api.loyalhealth.com/search/9eb91cea-158c-4433-b42d-fe512e05ca9c/3/1/search/all',
        params=params,
        headers=headers,
    )

    # Process API response
    result = response.json()
    if "providers" in result and len(result["providers"]) > 0:
        for provider in result["providers"]:
            Full_Name = provider.get("displayName", "N/A")
            Doctor_Profile_URL = f'https://www.andalusiahealth.com/find-a-doctor/provider/{provider.get("entityId", "")}'
            Phone_Number = provider.get("officePhoneNumber", "N/A")
            rating_data = provider.get("rating", {})
            acceptingNewPatients = provider.get("acceptingNewPatients", "N/A")
            employment_provider = provider.get("auditLogEntityType", "N/A")

            # Extract address details
            locations = provider.get("locations", {}).get("locations", [])
            if locations:
                location = locations[0]
                address_parts = [
                    location.get("locationName"),
                    location.get("address1"),
                    location.get("address2"),
                    location.get("city"),
                    location.get("state"),
                    location.get("zip")
                ]
                address = ", ".join(filter(None, address_parts))  # Remove empty values
            else:
                address = "N/A"

            # Store extracted data in a dictionary
            doctor_data = {
                "Name": Full_Name,
                "Profile_URL": Doctor_Profile_URL,
                "Phone": Phone_Number,
                "Address": address,
                "Rating": rating_data.get("rating", 0.0),
                "Rating_Count": rating_data.get("ratingCount", 0),
                "Review_Count": rating_data.get("reviewCount", "None"),
                "Accept_New_Patients": acceptingNewPatients,
                "Employed_Provider": employment_provider
            }

            doctors.append(doctor_data)

# Insert data into MongoDB Atlas
# if doctors:
#     collection.insert_many(doctors)
#     print(f"Inserted {len(doctors)} doctor records into MongoDB Atlas.")

# Convert to DataFrame
df = pd.DataFrame(doctors)

# (1) Total Number of Doctors
total_doctors = len(df)
print(f"Total Number of Doctors: {total_doctors}")

#(ii) Total Number of Doctors with Ratings
doctors_with_ratings = collection.count_documents({"Rating": {"$gt": 0}})
print(f"Doctors with Ratings: {doctors_with_ratings}")

#(iii) Doctors Having the Same Phone Number
pipeline = [
    {"$group": {"_id": "$Phone", "count": {"$sum": 1}, "doctors": {"$push": "$Name"}}},
    {"$match": {"count": {"$gt": 1}}}
]
duplicate_phones = list(collection.aggregate(pipeline))

print(f"Doctors with the same phone number: {duplicate_phones}")

#(iv) Doctors with More Than One Location
pipeline = [
    {"$group": {"_id": "$Name", "location_count": {"$sum": 1}}},
    {"$match": {"location_count": {"$gt": 1}}}
]
multiple_locations = list(collection.aggregate(pipeline))

print(f"Doctors with more than one location: {multiple_locations}")

#(i) Export Extracted Data to CSV
df = pd.DataFrame(list(collection.find({}, {"_id": 0})))  # Exclude MongoDB "_id"
df.to_csv("doctors_data.csv", index=False)
print("Exported doctors_data.csv")

#(ii) Export Extracted Data to JSON
df.to_json("doctors_data.json", orient="records", indent=4)
print("Exported doctors_data.json")

#(iii) Export Analysis Results
analysis_results = {
    "Total Doctors": total_doctors,
    "Doctors with Ratings": doctors_with_ratings,
    "Duplicate Phones": duplicate_phones,
    "Doctors with Multiple Locations": multiple_locations
}

with open("analysis_report.json", "w") as json_file:
    json.dump(analysis_results, json_file, indent=4)

print("Exported analysis_report.json")


