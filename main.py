from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

from selenium.webdriver.support.wait import WebDriverWait

import sendmusic as sm


def check_for_commands(wd):
    print("Waiting for commands...")
    chat = wd.find_elements(By.XPATH, "//button[@aria-label='Chat with everyone']")
    chat[0].click()
    time.sleep(1)
    chat_messages = wd.find_element(By.CSS_SELECTOR, "div[aria-live='polite']")
    while True:
        chat_messages_html = chat_messages.get_attribute("innerHTML")
        print(chat_messages_html)


# Launch the Chrome browser with options
opt = webdriver.ChromeOptions()
opt.add_argument('--disable-blink-features=AutomationControlled')  # Prevent detection
opt.add_argument('--start-maximized')
opt.add_argument("−−mute−audio")
# opt.add_argument("--headless")
opt.add_experimental_option("prefs", {  # Set media/notification permissions
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 0,
    "profile.default_content_setting_values.notifications": 1
})

meet_input = input("Enter Google Meet URL or meeting ID: ")

# Construct the full URL
if meet_input.startswith("https://"):
    url = meet_input
elif meet_input.startswith("meet.google.com/"):
    url = "https://" + meet_input
else:
    url = f"https://meet.google.com/{meet_input}"

sm.list_virtual_audio_devices()
device_index = int(input("Select the device index to stream audio to: "))

wd = webdriver.Chrome(options=opt)

# Load the Google Meet URL
wd.get(url)

# Handle permissions (microphone/camera)
try:
    time.sleep(5)  # Wait for permissions prompt (adjust if needed)
    allow_buttons = wd.find_elements(By.XPATH, "//span[text()='Allow']")
    for button in allow_buttons:
        button.click()
except Exception as e:
    print("Error handling permissions:", e)

wd.find_element(By.XPATH, "//span[text()='Continue without camera']").click()

# Find and fill the "Your name" input
try:
    name_input = wd.find_element(By.XPATH, "//input[@placeholder='Your name']")
    name_input.send_keys("MeetMusic - Github/Eta06")  # Replace with your actual name
    # name_input.send_keys(Keys.RETURN)  # Press Enter to confirm

except Exception as e:
    print("Error finding or filling the 'Your name' field:", e)

# Select the microphone and disable page sound
try:
    try:
        join_button = wd.find_element(By.XPATH, "//span[text()='Ask to join']")
        join_button.click()
    except Exception as e:
        print("Error joining meeting:", e)
        # Open settings menu
    for i in range(15, 0, -1):
        print("Please Allow MeetMusic In", i, "seconds")
        time.sleep(1)
    more_options_button = wd.find_elements(By.XPATH, "//button[@aria-label='More options']")
    # List how many elements
    for i in range(len(more_options_button)):
        try:
            more_options_button[i].click()
            break
        except Exception as e:
            pass
    time.sleep(1)
    settings_button = wd.find_element(By.XPATH, "//span[text()='Settings']")
    settings_button.click()
    time.sleep(2)  # Wait for settings to open
    try:
        microphone_button = wd.find_element(By.XPATH, "//div[text()='Microphone']//following-sibling::span//button")
        microphone_button.click()
        time.sleep(1)  # Allow the dropdown to appear
    except Exception as e:
        print("Error finding or clicking the microphone button:", e)

    microphone_options = wd.find_elements(By.XPATH, "//li[@role='menuitemradio']")
    for option in microphone_options:
        option_text = option.text
        if "CABLE Output (VB-Audio Virtual Cable)" in option_text:
            option.click()
            break
    time.sleep(2)

    # It should turn off the switch in there:
    noise_cancellation_button = wd.find_element(By.CSS_SELECTOR, "button[aria-label='Noise cancellation']")
    noise_cancellation_button.click()
    aria_checked_value = noise_cancellation_button.get_attribute("aria-checked")
    if aria_checked_value == "false":
        print("Noise cancellation successfully turned off")
    else:
        print("Failed to turn off noise cancellation")
    close_button = wd.find_element(By.CSS_SELECTOR,
                                   "button[aria-label='Close dialog'][data-mdc-dialog-action='close']")
    close_button.click()

    print("MeetMusic Ready!")

except Exception as e:
    print("Error selecting microphone or disabling sound:", e)

print("Playback started")
# sm.stream_audio_to_device("motivepeterpan.wav", device_index)
print("Playback Ended")

t1 = threading.Thread(check_for_commands(wd), name="check_for_commands")
t1.start()


# Keep the browser open until the user presses Enter
input("Press Enter to close the browser...")

# Close the browser
wd.quit()
