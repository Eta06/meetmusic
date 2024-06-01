from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import sendmusic as sm

# Launch the Chrome browser with options
opt = webdriver.ChromeOptions()
opt.add_argument('--disable-blink-features=AutomationControlled')  # Prevent detection
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {  # Set media/notification permissions
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
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

# Find and fill the "Your name" input
try:
    name_input = wd.find_element(By.XPATH, "//input[@placeholder='Your name']")
    name_input.send_keys("Github/Eta06")  # Replace with your actual name
    # name_input.send_keys(Keys.RETURN)  # Press Enter to confirm
except Exception as e:
    print("Error finding or filling the 'Your name' field:", e)

# Select the microphone and disable page sound
try:
    # Open settings menu
    more_options_button = wd.find_element(By.XPATH, "//button[@aria-label='More options']")
    more_options_button.click()
    time.sleep(1)
    settings_button = wd.find_element(By.XPATH, "//span[text()='Settings']")
    settings_button.click()
    time.sleep(2)  # Wait for settings to open
    """
    # Select Audio tab
    audio_tab = wd.find_element(By.XPATH, "//div[text()='Audio']")
    audio_tab.click()
    time.sleep(1)  # Wait for audio tab to load

    # Select desired microphone (replace 'Your Microphone Name' with your actual microphone name)
    microphone_dropdown = wd.find_element(By.XPATH, "//select[@name='selectedMicrophoneId']")
    microphone_dropdown.click()
    microphone_option = wd.find_element(By.XPATH, f"//option[text()='Your Microphone Name']")
    microphone_option.click()

    # Disable page sound (noise cancellation)
    sound_checkbox = wd.find_element(By.CSS_SELECTOR, "input[aria-labelledby='noiseCancellationLabel']")
    if sound_checkbox.is_selected():
        ActionChains(wd).move_to_element(sound_checkbox).click(sound_checkbox).perform()
    """
except Exception as e:
    print("Error selecting microphone or disabling sound:", e)

# Join the meeting
"""
try:
    join_button = wd.find_element(By.XPATH, "//span[text()='Join now']")
    join_button.click()
except Exception as e:
    print("Error joining meeting:", e)
"""

# Keep the browser open until the user presses Enter
input("Press Enter to close the browser...")

# Close the browser
wd.quit()
