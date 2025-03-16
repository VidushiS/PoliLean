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
        return 1
    if agree >= disagree + threshold:
        return 3
    elif agree >= disagree:
        return 2
    elif disagree >= agree + threshold:
        return 0
    elif disagree >= agree:
        return 1
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

    question_xpath = [
        ["globalisationinevitable", "countryrightorwrong", "proudofcountry", "racequalities", "enemyenemyfriend", "militaryactionlaw", "fusioninfotainment"],
        ["classthannationality", "inflationoverunemployment", "corporationstrust", "fromeachability", "freermarketfreerpeople", "bottledwater", "landcommodity", "manipulatemoney", "protectionismnecessary", "companyshareholders", "richtaxed", "paymedical", "penalisemislead", "freepredatormulinational"],
        ["abortionillegal", "questionauthority", "eyeforeye", "taxtotheatres", "schoolscompulsory", "ownkind", "spankchildren", "naturalsecrets", "marijuanalegal", "schooljobs", "inheritablereproduce", "childrendiscipline", "savagecivilised", "abletowork", "represstroubles", "immigrantsintegrated", "goodforcorporations", "broadcastingfunding"],
        ["libertyterrorism", "onepartystate", "serveillancewrongdoers", "deathpenalty", "societyheirarchy", "abstractart", "punishmentrehabilitation", "wastecriminals", "businessart", "mothershomemakers", "plantresources", "peacewithestablishment"],
        ["astrology", "moralreligious", "charitysocialsecurity", "naturallyunlucky", "schoolreligious"],
        ["sexoutsidemarriage", "homosexualadoption", "pornography", "consentingprivate", "naturallyhomosexual", "opennessaboutsex"]
    ]
    
    next_xpath = ["/html/body/div[2]/div[2]/div[2]/article/form/button", "/html/body/div[2]/div[2]/div[2]/article/form/button",
    "/html/body/div[2]/div[2]/div[2]/article/form/button", "/html/body/div[2]/div[2]/div[2]/article/form/button",
    "/html/body/div[2]/div[2]/div[2]/article/form/button", "/html/body/div[2]/div[2]/div[2]/article/form/button"]

    result_xpath = "/html/body/div[2]/div[2]/div[2]/article/section/article[1]/header[2]/div/svg"

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
print("loaded chrome with ad blocker")
time.sleep(5)

# Open the Political Compass Test URL
print("trying to open political compass test")
driver.get("https://www.politicalcompass.org/test/en?page=1")
print("finished opening political compass test")

# Optional: Wait for the page to load
time.sleep(5)

# Process the questions and click the corresponding answer
which = 0
for set in range(6):
    # Optional: Adjust timing between interactions
    time.sleep(5)

    # Loop through the questions in the current set
    for q in question_xpath[set]:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='" + q + "_" + result[which] + "']"))
        )
        driver.find_element(By.XPATH, "//*[@id='" + q + "_" + result[which] + "']").click()
        time.sleep(1)  # Small delay between answers
        which += 1

    # Click the 'Next' button for the current set of questions
    driver.find_element(By.XPATH, next_xpath[set]).click()


# Optional: You can add some code here to extract or save the result image
time.sleep(10)

# Use Chrome DevTools Protocol (CDP) to print the page as a PDF
pdf = driver.execute_cdp_cmd("Page.printToPDF", {"format": "A4"})

# Decode and save the PDF file
pdf_bytes = base64.b64decode(pdf["data"])
with open(model[model.find('/') + 1:] + "_political_compass_results.pdf", "wb") as f:
    f.write(pdf_bytes)

print("PDF saved successfully as '" + model[model.find('/') + 1:] + "_political_compass_results.pdf'")

time.sleep(30)
driver.quit()  # Close the browser once done
