import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException
import time
import random
import datetime
import colorama
import threading
from termcolor import colored
import asyncio

import getpass
import pickle
from cryptography import fernet
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import sys
import platform
from tinydb import TinyDB, Query, where

db = TinyDB(fr'upload_db.json')
User = Query()

colorama.init()

encryption_key = b'QW0DSBcFrSDnJ96xb1O9XzUgqGj5OgnQ3U0pDzNY1dc='


class Scraper:
    def __init__(self,upload_path, window,logout=False):
        self.figlet()

        self.upload_folder=upload_path

        self.logout = logout

        self.exit_program = False

        self.block_thread=False

        self.save_login_credentials()

        if window == "Y":
            self.stealth = False
        else:
            self.stealth = True

        self.seconds = time.perf_counter()
        self.sleep_ = 3
        self.status = "Starting bot"

        self.options = webdriver.ChromeOptions()
        os_detected = ""
        if platform.system() == "Darwin":
            chrome_data = fr"Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/Default"
            os_detected = "MAC OS"

        if platform.system() == "Windows":
            chrome_data = fr"C:\Users\{getpass.getuser()}\AppData\Local\Google\Chrome\User Data\Default"
            os_detected = "WINDOWS OS"
        if platform.system() == "Linux":
            chrome_data = fr"/home/{getpass.getuser()}/.config/google-chrome/default"
            os_detected = "LINUX OS"

        if not os_detected:
            print("Can't detect your operating system")

        else:
            print(colored(f"\n[{datetime.datetime.now()}] {os_detected} Detected ", "green"))
            self.options.add_argument(f"--user-data-dir={chrome_data}")

        self.options.add_argument("--lang=en_US")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--start-maximized")

        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False,
                 "profile.default_content_setting_values.notifications": 2}

        self.options.add_experimental_option("prefs", prefs)

        if self.stealth:
            print(colored("\nbrowser window mode disabled", "green"))
            self.options.add_argument("--headless")
        else:
            print(colored("\nbrowser window mode is enabled", "red"))

        chrome_service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=chrome_service, options=self.options)

        self.driver.set_window_size(900, 500)

        self.action = ActionChains(self.driver)

        def login_thread():
            asyncio.run(self.main_login())

        th = threading.Thread(target=login_thread)
        th.start()
        while True:
            #  check if login thread is running

            if not th.is_alive():
                if self.logout:
                    break
                else:
                    self.block_thread = False
                    asyncio.run(self.main())
                    break

    def save_login_credentials(self):
        encrypt_creds = fernet.Fernet(encryption_key)
        # db.update({"credentials": "true", "username": "jack", "password": "mypassword"})
        # db.insert({"credentials":"true","username":"jack","password":"mypassword"})
        # deleting user from db
        # db.remove(where('username') == 'jack')

        credentials = db.search(User.credentials == 'true')
        if credentials:
            # print(credentials)
            decrypt_credentials = credentials[0].get("encrypted").encode()

            decrypt_cryptography = encrypt_creds.decrypt(decrypt_credentials)
            decrypt_pickle2 = pickle.loads(decrypt_cryptography)
            self.username = decrypt_pickle2.get("username", "specify a username")
            self.password = decrypt_pickle2.get("password", "specify a password")

        else:
            print(colored(f"[{time.perf_counter()}] no logged in users found in database", "green"))
            print(colored(f"[{time.perf_counter()}] !password may not show on console as you type,hit Enter when done "
                          f"for each field", "cyan"), end="\n")

            self.username = input("Enter your username: ")
            self.password = getpass.getpass("Enter your password: ")

            credentials = {"username": self.username, "password": self.password}
            pickled_credentials = pickle.dumps(credentials)
            encrypted = encrypt_creds.encrypt(pickled_credentials)
            db.insert({"encrypted": encrypted.decode("utf-8"), "credentials": "true"})

    async def login(self, username, password):
        try:
            self.driver.get("https://www.instagram.com/")

            self.sleep_ = random.randrange(1, 4)
            self.seconds = time.perf_counter()
            self.status = "Getting instagram login page"

            await asyncio.sleep(self.sleep_)

            username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Sending username to login page"
            await asyncio.sleep(self.sleep_)
            username_field.send_keys(username)

            password_field = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.NAME, "password")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Sending password to login page"
            await asyncio.sleep(self.sleep_)
            password_field.send_keys(password)

            login_button = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Log In')]")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Logging in"
            await asyncio.sleep(self.sleep_)
            login_button.click()

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'check your username')]")))

                print(colored(
                    f"\n\nThe username you entered doesn't belong to an account. Please check your username and try again",
                    "red"))

                db.remove(where('credentials') == 'true')

            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException, NoSuchElementException) as e:
                pass

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'password was incorrect')]")))

                print(colored(f"\n\n Sorry broski, your password was incorrect. Please double-check your password.",
                              "red"))
                db.remove(where('credentials') == 'true')

            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                    StaleElementReferenceException, NoSuchElementException) as e:
                pass

            await self.click_save_creds()

        except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                StaleElementReferenceException, NoSuchElementException) as e:
            pass

        if self.logout:
            await self.logout_my_account()
            self.driver.quit()
            self.exit_program = True
        else:
            self.block_thread = True

    async def logout_my_account(self):
        account_tag = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]"
        account = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, account_tag)))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = f"Getting my account ( {self.username} ) info"
        await asyncio.sleep(self.sleep_)
        account.click()

        account_profile = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Log Out')]")))
        self.sleep_ = random.randrange(2, 7)
        self.seconds = time.perf_counter()
        self.status = f"Logging out of {self.username}"
        await asyncio.sleep(self.sleep_)
        account_profile.click()

    async def upload_post(self):
        print("\n Uploading posts \n")

        files_upload = []

        for file in os.listdir(self.upload_folder):
            if file=="hashtags.txt":
                with open(fr"{self.upload_folder}\{file}","r") as f:
                    hashtags=[hash_.strip() for hash_ in f.readlines()]
            else:
                files_upload.append(file)

        for file in files_upload:
            self.sleep_ = random.randrange(1,5)
            self.seconds = time.perf_counter()
            self.status = "getting upload page"
            await asyncio.sleep(self.sleep_)

            caption_=hashtags

            upload_button = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='New post']")))
            time.sleep(0.5)
            upload_button.click()

            upload = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "input[accept='image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime']")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "uploading file"
            await asyncio.sleep(self.sleep_)

            upload.send_keys(fr"{self.upload_folder}\{file}")

            filter_button = WebDriverWait(self.driver, 70).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Next')]")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Navigating to filters"
            await asyncio.sleep(self.sleep_)
            filter_button.click()

            next_button = WebDriverWait(self.driver, 70).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Next')]")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "Navigating to configure page"
            await asyncio.sleep(self.sleep_)
            next_button.click()

            caption = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "textarea[aria-label='Write a caption...']")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = "uploading file"
            await asyncio.sleep(self.sleep_)
            if not caption_:
                cap_ = " "
                caption.send_keys(cap_)

            else:
                for cap_ in caption_:
                    if "#" not in cap_:
                        cap_=f"#{cap_}"
                    caption.send_keys(cap_)

            share = WebDriverWait(self.driver, 70).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Share')]")))
            self.sleep_ = random.randrange(1, 5)
            self.seconds = time.perf_counter()
            self.status = f"Sharing {file} file"
            await asyncio.sleep(self.sleep_)
            share.click()
            start_upload=time.perf_counter()
            retries=0
            print("")
            reload=False
            while True:
                try:
                    WebDriverWait(self.driver,10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//*[contains(text(),'Your post has been shared.')]")))
                    break

                except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                        StaleElementReferenceException, NoSuchElementException) as e:
                    retries+=1

                sys.stdout.write(colored(f"\rTime elapsed [{datetime.timedelta(seconds=time.perf_counter()-start_upload)}]","green"))
                sys.stdout.flush()

                if retries>=30:
                    print(colored("\nsomething went wrong with your upload ", "red"))
                    try:
                        WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//*[contains(text(),'Discard')]"))).click()
                        break

                    except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
                            StaleElementReferenceException, NoSuchElementException) as e:
                        self.driver.get("https://www.instagram.com/")
                        reload=True
                        break

            print("")
            if not reload:
                close = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Close']")))
                self.sleep_ = random.randrange(1, 5)
                self.seconds = time.perf_counter()
                self.status = "Done uploading file"
                await asyncio.sleep(self.sleep_)
                close.click()

            self.sleep_bot(random.randrange(720,840),reason="next upload")

        self.exit_program=True
        self.driver.quit()
        quit()

    async def click_save_creds(self):

        save_button = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Not Now')]")))
        self.sleep_ = random.randrange(1, 5)
        self.seconds = time.perf_counter()
        self.status = "Getting pop up window"
        await asyncio.sleep(self.sleep_)
        save_button.click()
        #
        # try:
        #
        #     floating_win = WebDriverWait(self.driver,50).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Cancel')]")))
        #     self.sleep_ = random.randrange(1, 5)
        #     self.seconds = time.perf_counter()
        #     self.status = "clicked cancel popup window"
        #     await asyncio.sleep(self.sleep_)
        #     floating_win.click()
        #
        # except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException,
        #         StaleElementReferenceException, NoSuchElementException) as e:
        #
        #     self.sleep_ = random.randrange(1, 5)
        #     self.seconds = time.perf_counter()
        #     self.status = f"{e}"
        #     await asyncio.sleep(self.sleep_)

    def figlet(self):
        figlet_color = ["cyan", "yellow", "green", "magenta"]
        random.shuffle(figlet_color)
        print(colored('''                          
 _   _ _   _   ___   ___   _   _ _______ ___ ______ TM
| \ | | | | | | \ \ / | | | | | |____  .|_  |____  |
|  \| | | | | | |  V /| | | | | |    | |  | | _  | |
| |\  | |/ /_/ /| |\ \| |/ /_/ /     | |  | || | |_|
|_| \_|_______/ |_| \_|_______/      | |  | || |    
                                     |_|  |_||_|                                                        
''', f"{figlet_color[0]}"))

    def sleep_bot(self, timer=random.randrange(850, 1220), reason=""):
        sleep_time = timer
        lengths = [e for e in range(0, 10)]
        timer = time.perf_counter()
        char = "▓"
        for e in range(sleep_time):
            percentage = e / sleep_time * 100
            current_time = time.perf_counter() - timer
            time_remaining = datetime.timedelta(seconds=sleep_time - current_time)
            sleep_mins = str(datetime.timedelta(seconds=sleep_time)).split(":")[1]
            sys.stdout.write(
                colored(
                    f"\r[{sleep_mins} mins] {reason} sleep Timeout started | progress {time_remaining}{char} {round(percentage, 4)}%",
                    "green"))
            sys.stdout.flush()
            char_concatenate = round(percentage / 10) + 1

            char = "▓" * char_concatenate
            if len(char) in lengths:
                print("")
                lengths.remove(len(char))
            time.sleep(1)

    async def art(self):
        self.spinner = "..::::.."
        color = "yellow"

        while True:
            now_ = time.perf_counter() - self.seconds
            mins = datetime.timedelta(seconds=self.sleep_ - now_)
            char_ = ""

            if self.exit_program or self.block_thread:
                break
            for k, char in enumerate(self.spinner):
                try:
                    char_ += char
                    if "liked" in self.status:
                        color = "green"

                    if "you've liked" in self.status:
                        color = "cyan"
                    if "comment" in self.status:
                        color = "yellow"

                    sys.stdout.write(
                        colored(f"\r {char}{char}{char} ", color) + colored(f"{self.status} {str(mins)} ",
                                                                            color) + colored(
                            f"{char_.replace('.', f'{char}')}", color))
                    sys.stdout.flush()

                    await asyncio.sleep(0.1)
                except Exception as e:
                    await asyncio.sleep(0.01)

    async def main_login(self):
        task1 = asyncio.create_task(self.login(self.username, self.password))
        task2 = asyncio.create_task(self.art())

        await task1
        await task2

    async def main(self):
        # "Running second thread "
        task2 = asyncio.create_task(self.art())
        task3 = asyncio.create_task(self.upload_post())

        await task2
        await task3


def logout_user(upload_path, window,logout):
    encrypt_creds = fernet.Fernet(encryption_key)
    credentials = db.search(User.credentials == 'true')
    if credentials:

        Scraper(upload_path, window,logout=logout)

        decrypt_credentials = credentials[0].get("encrypted").encode()

        decrypt_cryptography = encrypt_creds.decrypt(decrypt_credentials)
        decrypt_pickle2 = pickle.loads(decrypt_cryptography)
        username = decrypt_pickle2.get("username", "specify a username")

        db.remove(where("credentials") == 'true')
        db.remove(where("last_settings") == 'true')

        print(colored(f"Logged out {username} and deleted all settings data ",
                      "yellow"))
        exit()
    else:
        print(colored("No logged in users ", "cyan"))
        print("\nlogin")


def user():
    encrypt_creds = fernet.Fernet(encryption_key)
    credentials = db.search(User.credentials == 'true')
    if credentials:
        decrypt_credentials = credentials[0].get("encrypted").encode()

        decrypt_cryptography = encrypt_creds.decrypt(decrypt_credentials)
        decrypt_pickle2 = pickle.loads(decrypt_cryptography)
        username = decrypt_pickle2.get("username", "specify a username")
        return username


def start():
    settings = db.search(User.last_settings == "true")

    if settings:
        settings[0].pop("last_settings")
        print(colored(settings[0], "green"))
        if settings[0].get("dont_ask") == "Y":
            print(colored(
                f"\nStarting .... \n\nTo logout of {user()} you can always run the following command and reset your settings \n\npython3 -m i_upload -logout",
                "cyan"))
            window = settings[0].get("window")
            upload_path = settings[0].get("upload_path")
            time.sleep(5)
        else:
            previous_setting = input(colored(
                "\nThese are your previous settings ,\ntype E for edit or Y to proceed with previous settings \n \nwould you like to proceed Y/E:",
                "yellow"))

            if previous_setting.capitalize() == "Y":
                window = settings[0].get("window")
                upload_path = settings[0].get("upload_path")

                save = input(r"Don't ask again Y\N:").capitalize()
                if save == "Y":
                    db.update(
                        {"last_settings": "true", "upload_path": upload_path,"dont_ask": save, "window": window})

                    print(colored(
                        f"\nStarting .... \n\nTo logout of {user()} you can always run the following command and reset your settings\n\npython3 -m i_upload -logout",
                        "cyan"))

            else:

                print(colored("\nEdit your settings", "cyan"))
                upload_path = input(r"Enter your upload folder path:")

                window = input(r"Enable browser window Y\N:").capitalize()
                print("")

                save = input(r"Don't ask again Y\N:").capitalize()

                db.update(
                    {"last_settings": "true", "upload_path":upload_path,
                     "dont_ask": save, "window": window})

    else:
        if len(sys.argv) >= 2:
            if sys.argv[1] == "-logout":
                print("no logged in users")
                exit()

        upload_path = input(r"Enter your upload folder path:")

        window = input(r"Enable browser window Y\N:").capitalize()

        db.insert(
            {"last_settings": "true", "upload_path": upload_path,"dont_ask": "N", "window": window})

    if len(sys.argv) >= 2:
        if sys.argv[1] == "-logout":
            print(colored("You'll be logged out of your account", "red"))
            logout_user(upload_path, window, True)
    else:
        Scraper(upload_path,window,)
