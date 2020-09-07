"""
This script extracts all the data required from the .html files and saves it into a .csv file.
"""

import csv

import lxml.html


# The next 2 lists must have the same length, since one will replace the other.
ACCENT_MARKS = ["á", "Á", "é", "É", "í", "Í", "ó", "Ó", "ú", "Ú"]
FRIENDLY_MARKS = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]


def load_files():
    """Reads the log file and extracts all files paths."""

    with open("log.txt", "r", encoding="utf-8") as temp_file:

        files_list = list()

        for item in temp_file.read().splitlines():
            file_name, file_date = item.split(",")
            files_list.append(("./states/" + file_name, file_date))

        return files_list


def parse_file(file_name, file_date):
    """Parses a .html file and extracts values of interest using lxml.

    Parameters
    ----------
    file_name : str
        The name of the file to be parsed.

    """

    with open(file_name, "r", encoding="utf-8") as temp_file:

        # Remove the time from from the file date.
        file_date = file_date.split()[0]

        # Parse the HTML document.
        html = lxml.html.fromstring(temp_file.read())

        name = html.xpath("//small[1]")[0].text.split("-")[0].lower().strip()

        clean_words = list()

        for word in name.split(" "):
            if word != "a" and word != "de" and word != "en" and not word.isdigit():
                clean_words.append(word)

        clean_name = clean_word(" ".join(clean_words))

        salary = html.xpath(
            "//strong[contains(text(),'Salario neto mensual:')]/following-sibling::span")[0].text.strip()

        clean_salary = int(float(salary.replace("$", "").replace(",", "")))

        hours = html.xpath(
            "//strong[contains(text(),'Horario de trabajo:')]/following-sibling::span")[0].text.split()

        start_hour = int(hours[0].replace(":", ""))
        end_hour = int(hours[2].replace(":", ""))

        if start_hour >= end_hour:
            hours_worked = ((end_hour+2400) - start_hour) / 100
        else:
            hours_worked = (end_hour - start_hour) / 100

        work_days = html.xpath(
            "//strong[contains(text(),'Días laborales:')]/following-sibling::span")[0].text.strip()

        monday = 1 if "L" in work_days else 0
        tuesday = 1 if "Ma" in work_days else 0
        wednesday = 1 if "Mi" in work_days else 0
        thursday = 1 if "J" in work_days else 0
        friday = 1 if "V" in work_days else 0
        saturday = 1 if "S" in work_days else 0
        sunday = 1 if "D" in work_days else 0

        days_worked = monday + tuesday + wednesday + \
            thursday + friday + saturday + sunday

        location = html.xpath(
            "//strong[contains(text(),'Ubicación:')]/following-sibling::span")[0].text.strip()

        state, municipality = location.split(",")

        education_level = html.xpath(
            "//strong[contains(text(),'Estudios Solicitados:')]/following-sibling::div")[0].text.strip()

        languages = html.xpath(
            "//strong[contains(text(),'Idiomas:')]/following-sibling::div")[0].text.strip()

        try:
            experience = html.xpath(
                "//strong[contains(text(),'Experiencia:')]/following-sibling::div")[0].text.strip()
        except:
            experience = "No especificada"

        try:
            contract_type = html.xpath(
                "//strong[contains(text(),'Tipo de contrato:')]/following-sibling::span")[0].text.strip()
        except:
            contract_type = "No especificado"

        data_list.append((file_date, clean_name, clean_salary, contract_type,
                          start_hour, end_hour, hours_worked, monday, tuesday,
                          wednesday, thursday, friday, saturday, sunday, days_worked,
                          state.strip(), municipality.strip(), education_level, experience,
                          languages))


def clean_word(word):
    """Cleans the word by replacing non-friendly characters.

    Parameters
    ----------
    word : str
        The word to be cleaned.

    Returns
    -------
    str
        The cleaned word.

    """

    for index, char in enumerate(ACCENT_MARKS):
        word = word.replace(char, FRIENDLY_MARKS[index])

    return word


if __name__ == "__main__":

    # We use multithreading to accelerate the reading of all files.
    data_list = list()
    data_list.append(["isodate", "offer", "salary", "contract_type", "start_hour",
                      "end_hour", "hours_worked", "monday", "tuesday", "wednesday",
                      "thursday", "friday", "saturday", "sunday", "days_worked",
                      "state", "municipality", "education_level", "experience", "languages"])

    for file_name, file_date in load_files():
        parse_file(file_name, file_date)

    with open("data.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows(data_list)
