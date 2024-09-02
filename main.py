import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# replace this link with the unit of videos you want to watch
url = "https://apclassroom.collegeboard.org/8/home?unit=4"

def read_passwords(file_path):
    file_path = 'passwords.txt'
    passwords = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Ignore empty lines and comments
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split('=', 1)
                passwords[key] = value
    return passwords

file_path = 'passwords.txt'
secrets = read_passwords(file_path)
email = secrets['EMAIL']
password = secrets['PASSWORD']

def waitToLoad(sleepTime):
    print(f"waiting {sleepTime} second(s) to load...")
    time.sleep(sleepTime)

def getVideoTime():
    try:
        stringTime = driver.find_element(By.CLASS_NAME, "w-playbar__time").text
        if not stringTime or ":" not in stringTime:
            raise ValueError(f"unexpected time format: {stringTime}")
        minutes, seconds = map(int, stringTime.split(":"))
        totalSeconds = minutes * 60 + seconds + 10
    except Exception as e:
        hover_element = driver.find_element(By.CLASS_NAME, "w-bottom-bar")
        action = ActionChains(driver)
        action.move_to_element(hover_element).perform()
        print(f"Error: {e}")
        waitToLoad(1)
        totalSeconds = getVideoTime()
    return totalSeconds

def secondsToMinutes(seconds):
    return f"{int(seconds / 60)}:{seconds % 60}"

driver = webdriver.Chrome()
driver.get(url)

# Wait for page to load
waitToLoad(8)

# Log In
if driver.current_url.startswith("https://account.collegeboard.org/login"):
    print("logging in...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cb-btn-primary"))).click()
    waitToLoad(4)
    driver.find_element(By.ID, "idp-discovery-username").send_keys(email)
    waitToLoad(1)
    driver.find_element(By.ID, "idp-discovery-submit").click()
    waitToLoad(2)
    driver.find_element(By.ID, "okta-signin-password").send_keys(password)
    waitToLoad(1)
    driver.find_element(By.ID, "okta-signin-submit").click()
    waitToLoad(8)
    print("logged in")


# Expands video List
driver.find_element(By.XPATH, "//button[./div[text()='Expand all']]").click()
print("expanded video list")
waitToLoad(1)

videoNumber = 1

while True:

    try:
        driver.find_element(By.XPATH, f"(//div[contains(@class, 'flex flex-row items-center py-6')])[{videoNumber}]").click()
        print(f"opened video {videoNumber}")
        waitToLoad(2)
    except:
        # exits if there are no more videos to watch
        break

    # Get Video Length
    waitToLoad(4)
    totalSeconds = getVideoTime()
    
    # Set 2x speed
    print("setting video speed...")
    driver.find_elements(By.CLASS_NAME, "w-vulcan-icon-wrapper")[4].click()
    waitToLoad(1)
    driver.find_element(By.ID, "w-Speed-accordion-title").click()
    waitToLoad(1)
    driver.find_element(By.XPATH, "//label[contains(text(), '2x')]").click()
    print("video speed sent")
    waitToLoad(1)

    # Play Video
    try:
        driver.find_element(By.CLASS_NAME, "w-vulcan-icon-wrapper").click()
        print("playing video...")
    except:
        print("error playing video")

    waitToLoad(2)

    #Wait for video to complete
    currentTime = 0
    pastTime = 0
    while True:
        currentTime = getVideoTime()
        time.sleep(1)
        print(f"{secondsToMinutes(currentTime)} / {secondsToMinutes(totalSeconds)}   :   {secondsToMinutes(totalSeconds - currentTime)} remaining")
        if currentTime == pastTime:
            break
        pastTime = currentTime

    waitToLoad(4)
    driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()

    print(f"watched video {videoNumber}")
    waitToLoad(1)

    # select next video
    videoNumber += 1

print("watched all videos...closing program")