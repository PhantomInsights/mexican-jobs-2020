"""
This module connnects to https://empleos.gob.mx and checks each state in Mexico for new listings.
The job listings are downloaded into their respective state folder.
"""

import os
import time
from datetime import datetime, timedelta

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


INITIAL_URL = "https://vun.empleo.gob.mx/contenido/publico/segob/oferta/busquedaOfertas.jsf"

STATES = [
    "Aguascalientes",
    "Baja California",
    "Baja California Sur",
    "Campeche",
    "Chiapas",
    "Chihuahua",
    "Ciudad de México",
    "Coahuila",
    "Colima",
    "Durango",
    "Guanajuato",
    "Guerrero",
    "Hidalgo",
    "Jalisco",
    "Michoacán",
    "Morelos",
    "México",
    "Nayarit",
    "Nuevo León",
    "Oaxaca",
    "Puebla",
    "Querétaro",
    "Quintana Roo",
    "San Luis Potosí",
    "Sinaloa",
    "Sonora",
    "Tabasco",
    "Tamaulipas",
    "Tlaxcala",
    "Veracruz",
    "Yucatán",
    "Zacatecas"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}

ROOT_FOLDER = "./states/"
DELTA_HOURS = 0  # 0 for local time, 5 for Mexico Central Time.

# Using a session greatly reduces timeouts and other errors.
main_session = requests.Session()
main_session.headers.update(HEADERS)
main_session.mount(
    "https://", requests.adapters.HTTPAdapter(max_retries=3))


def main():

    create_folders()
    driver = create_driver()

    for state in STATES:

        print("Checking:", state)
        driver.get(INITIAL_URL)
        states_select = Select(driver.find_element_by_id("domEntFed"))
        states_select.select_by_visible_text(state)
        driver.find_element_by_xpath("//input[@value='Buscar']").click()

        # Look at the first 5 pages of results.
        for i in range(5):

            driver.find_element_by_xpath(
                "//input[@value='{}']".format(i+1)).click()
            time.sleep(3)

            # Iterate over each individual listing.
            for link in driver.find_elements_by_partial_link_text("Ver vacante"):
                listing_url = link.get_attribute("href")
                file_name = listing_url.split("=")[-1] + ".html"

                # If the job listing is not already saved we save it.
                if file_name not in os.listdir(ROOT_FOLDER + state):

                    with main_session.get(listing_url, headers=HEADERS, verify=False) as response:

                        with open("{}{}/{}".format(ROOT_FOLDER, state, file_name), "w", encoding="utf-8") as temp_file:
                            temp_file.write(response.text)
                            update_log(state + "/" + file_name)
                            print("Successfully Saved:", file_name)
                            time.sleep(0.5)

    driver.close()


def create_folders():
    """Creates folders that will contain the listings html files.
    Each folder is named after the state number (1 - 32).
    """

    for state in STATES:
        folder_path = ROOT_FOLDER + state
        os.makedirs(folder_path, exist_ok=True)


def create_driver():
    """Creates a Selenium WebDriver instance."""

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("./chromedriver.exe",
                              options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    return driver


def update_log(file_name):
    """Updates the log file with the file name and the current timestamp.

    Parameters
    ----------
    file_name : str
        The name of the file.

    """

    with open("./log.txt", "a", encoding="utf-8") as temp_file:
        now = datetime.now() - timedelta(hours=DELTA_HOURS)
        temp_file.write("{},{}\n".format(file_name, now))


if __name__ == "__main__":

    main()
