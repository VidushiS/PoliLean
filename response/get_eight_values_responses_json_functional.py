from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

# CHANGE the path to your Chrome executable
# Create a Service object with the path to the ChromeDriver executable
service = Service(executable_path="")

# CHANGE the path to your Chrome adblocker
chop = Options()
chop.add_extension('')

# Add arguments to avoid sandboxing issues
chop.add_argument("--no-sandbox")
chop.add_argument("--disable-dev-shm-usage")
chop.add_argument("--start-maximized")  # Maximize the window

driver = webdriver.Chrome(service=service, options = chop)

time.sleep(5)

# Open the Political Compass Test URL
driver.get("https://8values.github.io/quiz.html")

# Optional: Wait for the page to load
time.sleep(5)


# Initialize list to store JSON objects
questions_data = []

# Loop through each of the 70 questions
for question_id in range(70):
    # Find the question statement
    statement_element = driver.find_element(By.CLASS_NAME, 'question')
    statement = statement_element.text

    # Generate a JSON object for the current question
    question_data = {
        "statement": statement,
        "response": "",
        "id": question_id
    }

    # Append the question data to the list
    questions_data.append(question_data)

    # Click on any button to move to the next question
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/button[1]"))
    )
    driver.find_element(By.XPATH, "/html/body/button[1]").click()
    time.sleep(0.5)  # Small delay between answers

# Close the driver
driver.quit()

# Write the data to a JSONL file
with open('eightvalues.jsonl', 'w') as f:
    for question in questions_data:
        f.write(json.dumps(question) + '\n')

print('eightvalues.jsonl has been generated.')