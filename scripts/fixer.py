"""
This script fixes corrupted files by redownloading them.
"""

import os
import time

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


MAIN_FOLDER = "./states/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}


def main():
    """Iterate over each folder and check each file."""

    for folder in os.listdir(MAIN_FOLDER):

        for file in os.listdir(MAIN_FOLDER + folder):

            full_path = MAIN_FOLDER + folder + "/" + file

            if os.stat(full_path).st_size <= 20000:
                redownload(full_path)

            check_file(full_path)


def redownload(full_path):
    """Redownload the specified file.

    Parameters
    ----------
    full_path : str
        The relative file path of the HTML document.

    """

    file_id = full_path.split("/")[-1].replace(".html", "")
    base_url = f"https://www.empleo.gob.mx/{file_id}-oferta-de-empleo-de-empleado-test-"

    with requests.get(base_url, headers=HEADERS, verify=False) as response:

        with open(full_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(response.text)
            print("Redownloaded:", full_path)
            time.sleep(1)


def check_file(full_path):
    """Check if the specified file was incorrectly downloaded.

    Parameters
    ----------
    full_path : str
        The relative file path of the HTML document.

    """

    with open(full_path, "r", encoding="utf-8") as temp_file:

        file_text = temp_file.read()

        if "Error 404" in file_text:
            print("Error", full_path)
            redownload(full_path)


if __name__ == "__main__":

    main()
