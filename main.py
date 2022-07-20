from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas

# fill in variables
CHROME_DRIVER_PATH = "right click on file > copy file path"
EMAIL = "email"
PASSWORD = "password"
ADD_TO_PROFILE = 1  # add to first by default

CSV_TO_FORMAT = "NetflixViewingHistory.csv"  # this should be the default filename when you download the file
FORMATTED_CSV_TO_SEARCH = "formatted_netflix_movies.csv"
NETFLIX_URL = "https://www.netflix.com/browse"


def netflix_add_to_list(email, password, chrome_driver_path, csv_to_search):
    # convert csv to ls
    df = pandas.read_csv(csv_to_search)
    shows = []
    for title in df.title:
        shows.append(title)

    ser = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=ser)
    driver.get(NETFLIX_URL)

    # sign in
    email_field = driver.find_element(By.CSS_SELECTOR, '#id_userLoginId')
    password_field = driver.find_element(By.CSS_SELECTOR, '#id_password')
    sign_in_btn = driver.find_element(By.CSS_SELECTOR, '.login-button')

    email_field.send_keys(email)
    password_field.send_keys(password)
    sign_in_btn.click()

    sleep(2)
    profile_names = driver.find_elements(By.CSS_SELECTOR, '.choose-profile .profile-link')
    try:
        profile_names[ADD_TO_PROFILE - 1].click()
    except IndexError:
        print(f"Profile {ADD_TO_PROFILE} does not exist.")
        driver.quit()
        return

    for show in shows:
        # search tab state unchanged after show not found so skip this line of code when exception thrown
        try:
            sleep(2)
            search_button = driver.find_element(By.CSS_SELECTOR, '.searchTab')
            search_button.click()
        except NoSuchElementException:
            pass

        sleep(1)
        search_bar = driver.find_element(By.CSS_SELECTOR, '#searchInput')
        search_bar.send_keys(show)

        # if show not found skip to next show
        try:
            sleep(2)
            first_search = driver.find_element(By.CSS_SELECTOR, '.slider-item-0')
            first_search.click()
        except NoSuchElementException:
            print(f"{show} not found")

            sleep(1)
            clear_search_bar = driver.find_element(By.CSS_SELECTOR, '.icon-close')
            clear_search_bar.click()
            continue

        add_to_list = driver.find_element(By.CSS_SELECTOR, '.ptrack-content button')
        add_to_list.click()
        add_to_list.send_keys(Keys.ESCAPE)

        sleep(1)
        clear_search_bar = driver.find_element(By.CSS_SELECTOR, '.icon-close')
        clear_search_bar.click()

    driver.quit()


def format_netflix_csv(file):
    df = pandas.read_csv(file)
    df.Title.dropna(inplace=True)

    # there's prob a better way to do this
    formatted_title_column = []
    for title in df.Title:
        if title == " ":  # stupid space in one entry won't go away unless i do this
            continue
        formatted_title_column.append(title.split(":")[0])

    formatted_df = pandas.DataFrame(formatted_title_column, columns=['title'])
    formatted_df.drop_duplicates(inplace=True)
    formatted_df.dropna(inplace=True)  # just in case
    formatted_df.to_csv('formatted_netflix_movies.csv')


format_netflix_csv(CSV_TO_FORMAT)
netflix_add_to_list(EMAIL, PASSWORD, CHROME_DRIVER_PATH, FORMATTED_CSV_TO_SEARCH)
