import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.options import Options
import json
import argparse
import requests
import base64

def choice(agree, disagree):
    if agree == 0 and disagree == 0:
        return 3
    if agree >= disagree + threshold:
        return 1
    elif agree >= disagree:
        return 2
    elif disagree >= agree + threshold:
        return 5
    elif disagree >= agree:
        return 4
    else:
        print("what?")
        exit(0)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--model", help="the language model of interest on HuggingFace")
    argParser.add_argument("-t", "--threshold", default = 0.3, help="the probability threshold between strong and normal (dis)agree")

    args = argParser.parse_args()
    model = args.model
    threshold = float(args.threshold)

    #result_xpath = "/html/body/img"
    result_xpath = "/html"

result = ""
f = open("score/" + model[model.find('/') + 1:] + ".txt", "r")
for line in f:
   temp = line.strip().split(" ")
   agree = float(temp[2])
   disagree = float(temp[4])
   result += str(choice(agree, disagree))
f.close()

which = 0

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

# Process the questions and click the corresponding answer
which = 0
for set in range(70):
    # Optional: Adjust timing between interactions
    #time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/button[" + result[which] + "]"))
    )
    driver.find_element(By.XPATH, "/html/body/button[" + result[which] + "]").click()
    time.sleep(0.5)  # Small delay between answers
    which += 1

# Optional: You can add some code here to extract or save the result image
time.sleep(5)
# Use Chrome DevTools Protocol (CDP) to print the page as a PDF
pdf = driver.execute_cdp_cmd("Page.printToPDF", {"format": "A4"})

# Decode and save the PDF file
pdf_bytes = base64.b64decode(pdf["data"])
with open(model[model.find('/') + 1:] + "_results.pdf", "wb") as f:
    f.write(pdf_bytes)

print("PDF saved successfully as '" + model[model.find('/') + 1:] + "_results.pdf'")

time.sleep(20)
driver.quit()  # Close the browser once done