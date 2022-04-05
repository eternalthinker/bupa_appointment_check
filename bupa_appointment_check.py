'''
Steps to run:
  - `python3 -m venv venv`
  - `source ./venv/bin/activate`
  - `pip install -r requirements.txt`
  - Edit User options below
  - `python3 bupa_appointment_check.py`
'''

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

## User options ##
POSTCODE = "2000"
ASSESSMENTS = [
    "501"
]
CURRENT_DATE = datetime.strptime("01/04/2022", "%d/%m/%Y")
# Do not show browser
HEADLESS = True
## End of User options ##

# HTML ID suffixes of radio buttons, checkboxes
location_id_map = {
    "Sydney": "168",
    "Parramatta": "60",
}
assessment_id_map = {
    "501": "489",
}

options = Options()
options.headless = HEADLESS
driver = webdriver.Chrome(options=options)
driver.get("https://bmvs.onlineappointmentscheduling.net.au/oasis/")
wait = WebDriverWait(driver, 20)

is_first_time = True

# Start with a new individual appointment
individual_appt_button = wait.until(
    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnInd")))
individual_appt_button.click()

while True:
    for location in location_id_map.keys():
        # Enter postcode
        postcode_input = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_SelectLocation1_txtSuburb")))
        postcode_input.send_keys(POSTCODE)

        # Proceed to list of locations
        location_search_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='postcode-search']/input[@value='Search']")))
        location_search_button.click()

        # Select current location
        location_radio_id = "rbLocation{}".format(location_id_map[location])
        location_radio_button = wait.until(
            EC.element_to_be_clickable((By.ID, location_radio_id)))
        location_radio_button.click()

        # Dismiss alert
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except:
            # No alert found
            pass

        # Proceed to medical assessments page
        to_assessments_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnCont")))
        to_assessments_button.click()

        # For the first pass, check the required medical assessments
        if is_first_time:
            is_first_time = False
            # Check the necessary medical assessments
            for assessment in ASSESSMENTS:
                assessment_check_id = "chkClass1_{}".format(
                    assessment_id_map[assessment])
                assessment_checkbox = wait.until(
                    EC.element_to_be_clickable((By.ID, assessment_check_id)))
                assessment_checkbox.click()

        # Proceed to available dates
        to_dates_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnCont")))
        to_dates_button.click()

        # Read earliest available date
        date_input = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_SelectTime1_txtAppDate")))
        available_date_str = date_input.get_attribute("value")
        available_date = datetime.strptime(available_date_str, "%d/%m/%Y")

        if available_date < CURRENT_DATE:
            print("{}: Earlier date found for {}! ----> {}".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), location, available_date_str))
            # For Mac
            os.system("say Earlier date found for {}".format(location))

        back_to_assessments_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='continue-button']/button[@class='white-button']")))
        back_to_assessments_button.click()

        back_to_locations_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='continue-button']/button[@class='white-button']")))
        back_to_locations_button.click()

input("Press any key to close..")
driver.close()
