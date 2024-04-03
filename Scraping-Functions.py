import os, time
from Backend import Database_Modifier

with open("api-key.txt", "r") as file:
    key = file.read()


def scrape_Google_Maps_Long_Lat():
    import pyperclip

    pyperclip.waitForNewPaste(10)

    return_list = []

    loop_bool = True

    while loop_bool:
        try:
            current_clipboard = pyperclip.paste()
            print("Copying: " + current_clipboard)

            return_list.append(current_clipboard)

            print("Appending: " + pyperclip.paste())

            pyperclip.waitForNewPaste(10)
        except pyperclip.PyperclipTimeoutException:
            print("Complete")

            loop_bool = False
    print("The following cooderinates were recorded during this session:")
    print(return_list)
    return return_list


def coordinates_To_Address(lat_long_string):
    if len(lat_long_string) < 15:
        return
    import requests, json

    google_JSON_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat_long_string.replace(" ",
                                                                                                            "") + "&key=" + key

    api_data = json.loads(requests.get(google_JSON_url).text)
    print(api_data)

    street_number = api_data['results'][0]["formatted_address"]
    town_state_zip = api_data['results'][3]["formatted_address"]
    county = api_data['results'][5]["formatted_address"]

    print(street_number)
    print(town_state_zip)
    print(county)

    print("Visual: ")
    print("http://maps.google.com/maps?q=&layer=c&cbll=" + lat_long_string.replace(" ", "") + "&cbp=11,0,0,0,0")

    return [street_number, town_state_zip, county, lat_long_string]


def patriotProperties_Scraper(street_num, street_name):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import pyperclip

    import pyautogui, time

    driver = webdriver.Firefox()

    driver.get("https://billerica.patriotproperties.com/search.asp")
    driver.maximize_window()
    all_frames = driver.find_elements(By.XPATH, "//frame")

    time.sleep(2)

    frame_middle = driver.find_element(By.XPATH, '//frame[@name="middle"]')
    driver.switch_to.frame(frame_middle)

    elem = driver.find_element(By.NAME, "SearchVal1")
    elem.clear()
    elem.send_keys(street_name)

    elem = driver.find_element(By.NAME, "SearchVal2")
    elem.clear()
    elem.send_keys(street_num)
    elem.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)
    time.sleep(2)

    print(driver.page_source)

    driver.switch_to.default_content()

    frame_bottom = driver.find_element(By.XPATH, '//frame[@name="bottom"]')
    driver.switch_to.frame(frame_bottom)

    print("Finding on page: " + street_num + " " + street_name.upper())

    link = driver.find_element(By.LINK_TEXT, street_num + " " + street_name.upper())

    link.click()

    # pyautogui.click(33, 272)

    time.sleep(2)

    pyautogui.click(103, 177)

    time.sleep(3)

    pyautogui.rightClick(103, 177)
    pyautogui.click(160, 375)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    if not os.path.exists("static/Property Reports/" + street_name):
        os.makedirs("static/Property Reports/" + street_name)

    with open("static/Property Reports/" + street_name + "/" + street_num + " " + street_name + ".html", "w",
              encoding='utf-8') as f:
        f.write(pyperclip.paste())

    driver.close()

    # Used for mass scraping


class Information_Retrieval_Tool:
    def __init__(self):
        self.arrest_url_log = "https://police.billericaps.com/index.php/logs/"
        self.home_information_url = "https://billerica.patriotproperties.com/default.asp"
        self.billerica_map_url = "https://www.google.com/maps/place/Billerica,+MA/@42.5597003,-71.3105115,13z/data=!3m1!4b1!4m6!3m5!1s0x89e3a194a66bad0d:0x8d7e8efdb1611c11!8m2!3d42.5584218!4d-71.2689461!16zL20vMHR6emg?entry=ttu"
        self.neighborhood_url = "https://www.google.com/maps/@42.5337476,-71.2537305,17.67z?entry=ttu"
        self.coordinates_list = []
        self.address_information_list = []

    def scrape_home_information(self):
        from selenium import webdriver
        driver = webdriver.Firefox()

        driver.get(self.neighborhood_url)
        driver.maximize_window()

        self.coordinates_list = scrape_Google_Maps_Long_Lat()

        driver.close()

        for long_lat in self.coordinates_list:
            self.address_information_list.append(coordinates_To_Address(long_lat))

        print(self.address_information_list)

        for address in self.address_information_list:
            address_number = address[0].split()[0]
            address_street = address[0].split()[1] + " " + address[0].split()[2][:-1]

            patriotProperties_Scraper(address_number, address_street)


# Information_Retrieval_Tool().scrape_home_information()


def jurisdiction_addresses_to_patriot_properties():
    with open("Jurisdiction Addresses.csv", "r") as out_file:
        for row in out_file:
            # print(row)
            line = row.split()
            # print(line)
            try:
                street_num = line[0]
                street_name = line[1] + " " + line[2][:-1]
                patriotProperties_Scraper(street_num, street_name)

            except IndexError:
                pass


def arrest_Log_Loop():
    test_loop = []
    for directory in os.listdir("Forms/Billerica PD Arrest Records"):
        test_loop.append(scrape_Arrest_Log("Forms/Billerica PD Arrest Records/" + directory))

    for val1 in test_loop:
        for val2 in val1:
            Database_Modifier().check_If_Table_Exists("Arrest_Records", val2.keys())
            Database_Modifier().create_Database_Row("Arrest_Records", val2)
            print(val2)


def scrape_Arrest_Log(pdf_file):
    from PyPDF2 import PdfReader
    import json

    reader = PdfReader(pdf_file)

    page = reader.pages[0].extract_text().split("\n")

    loop_dict = {"Name": "",
                 "Age": "",
                 "Offense": "",
                 "Gender": "",
                 "Date of Arrest": "",
                 "Address": ""}
    return_list = []

    for item in page:

        if "Name:" in item:
            offense_text = item[: item.index("Name:")].replace("   ", " ").replace("_", "")

            name_text = item[item.index("Name:"): item.index("Age:")].replace("   ", " ")[6:].strip()

            age_text = item[item.index("Age:"):item.index("Sex:")].strip()[5:]

            gender_text = item[item.index("Sex:"):][5:]

            loop_dict["Name"] = name_text
            loop_dict["Age"] = age_text
            loop_dict["Offense"] = offense_text
            loop_dict["Gender"] = gender_text

        elif "Date of Arrest" in item:
            date_of_arrest = item[17:]

            loop_dict["Date of Arrest"] = date_of_arrest

        elif "Address" in item:
            address = item[10:]
            loop_dict["Address"] = address

        elif item == "Charged with: ":
            return_list.append(dict(loop_dict))

    return return_list


def scrape_Billerica_Business_Listing():
    import requests
    from bs4 import BeautifulSoup
    import re

    index = 2

    return_Dict = {}
    other_dict = {}
    while True:
        dynamic_url = "https://www.town.billerica.ma.us/BusinessDirectoryii.aspx?ysnShowAll=0&lngNewPage=" + str(
            index) + "&txtLetter=&txtZipCode=&txtCity=&txtState=&txtBusinessName=&lngBusinessCategoryID=0&txtCustomField1=&txtCustomField2=&txtCustomField3=&txtCustomField4=&txtAreaCode="

        soup = BeautifulSoup(requests.get(dynamic_url).text, 'html.parser')



        for link in soup.find_all('span')[31:-28]:
            line_item = link.text.replace("\n", "").replace("\t", "")

            return_Dict[line_item] = {"Address":"","Phone Number":"","Website":"","Description":""}



        try:
            for row in soup.find_all("tr")[6:-1]:
                business_information = row.text.replace("\n", "").replace("\t", "").strip()
                #print(business_information)
                business_name = row.contents[1].contents[1].contents[0]
                address = row.contents[1].contents[3]
                phone_number = row.contents[1].contents[10].text

                other_dict[business_name] = {"Address":address,"Phone Number":phone_number}
        except IndexError:
            pass

        index += 1
        print(other_dict)
        time.sleep(2)









# print(soup.prettify())


#scrape_Billerica_Business_Listing()
