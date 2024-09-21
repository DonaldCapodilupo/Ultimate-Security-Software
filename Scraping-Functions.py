import os, time
from Backend import Database_Modifier
import pandas as pd

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

            return_Dict[line_item] = {"Address": "", "Phone Number": "", "Website": "", "Description": ""}

        try:
            for row in soup.find_all("tr")[6:-1]:
                business_information = row.text.replace("\n", "").replace("\t", "").strip()
                # print(business_information)
                business_name = row.contents[1].contents[1].contents[0]
                address = row.contents[1].contents[3]
                phone_number = row.contents[1].contents[10].text

                other_dict[business_name] = {"Address": address, "Phone Number": phone_number}
        except IndexError:
            pass

        index += 1
        print(other_dict)
        time.sleep(2)


def scrape_Facebook_Friends():
    from bs4 import BeautifulSoup

    html_file = open("C:\\Users\Don\AppData\Roaming\JetBrains\PyCharm2020.2\scratches\guitar chart.html",
                     encoding='utf8')

    soup = BeautifulSoup(html_file, 'html.parser')

    list_of_friends = []

    i = 0
    for person_name in soup.find_all("div", {"class": "x1hq5gj4"}):
        list_of_friends.append(person_name.text)
        print(person_name.text)
        i += 1
    print(str(i) + " friends were scraped")
    print(list_of_friends)

    # print(soup)


def scrape_Facebook_Copy_Paste():
    import pyperclip

    return_dict = {
        "Full Name": [],
        "Education History": {
            "College": [],
            "High School": []},
        "Places Lived": [],
        "Contact Info": {
            "Phone Numbers": [],
            "Websites & Social Medias": [],
            "Basic Info": []
        },
        "Relationships": [],
        "Family Members": [],

    }

    while True:
        try:
            print("Waiting for copy")
            pyperclip.waitForNewPaste(10)

            current_clipboard = pyperclip.paste()
            # print("Copying: " + current_clipboard)

            copied_information = current_clipboard.split("\r\n")

            return_dict["Full Name"] = copied_information[3]

            index = 7
            if copied_information[6] == "Work":
                for place_worked in copied_information[7:]:
                    index += 1
                    if place_worked == "College":
                        work_history = copied_information[7:index - 1]
                        return_dict["Work History"] = work_history
                        break

                college_index = index
                for colleges_attended in copied_information[college_index:]:
                    index += 1
                    if colleges_attended == "High school":
                        return_dict["Education History"]["College"] = copied_information[college_index:index - 1]
                        break

                high_school_index = index

                for high_schools_attended in copied_information[high_school_index:]:
                    index += 1
                    if high_schools_attended == "Friends":
                        return_dict["Education History"]["High School"] = copied_information[
                                                                          high_school_index:index - 1]
                        break
            elif copied_information[6] == "Places lived":
                for place_lived in copied_information[7:]:
                    index += 1
                    if place_lived == "Friends":
                        work_history = copied_information[7:index - 1]
                        return_dict["Places Lived"] = work_history
                        break
            elif copied_information[6] == "Contact info":
                for phone_number in copied_information[7:]:
                    index += 1
                    if phone_number == "Websites and social links":
                        contact_info = copied_information[7:index - 1]
                        return_dict["Contact Info"]["Phone Numbers"] = contact_info
                        break

                website_index = index
                for website_or_social in copied_information[website_index:]:
                    index += 1
                    if website_or_social == "Basic info":
                        return_dict["Contact Info"]["Websites & Social Medias"] = copied_information[
                                                                                  website_index:index - 1]
                        break

                basic_info_index = index
                for basic_info in copied_information[basic_info_index:]:
                    index += 1
                    if basic_info == "Basic info":
                        return_dict["Contact Info"]["Basic Info"] = copied_information[website_index:index - 1]
                        break

            elif copied_information[6] == "Relationship":
                for relationship in copied_information[7:]:
                    index += 1
                    if relationship == "Family members":
                        relationship_info = copied_information[7:index - 1]
                        return_dict["Relationships"] = relationship_info
                        break

                family_members_index = index
                for website_or_social in copied_information[family_members_index:]:
                    index += 1
                    if website_or_social == "Friends":
                        return_dict["Family Members"] = copied_information[family_members_index:index - 1]
                        break

            print(return_dict)


        except pyperclip.PyperclipTimeoutException:
            print("Complete")

            return False


def manually_Record_Address_Vehicles():
    for address in os.listdir("static/Property Reports/Elizabeth Rd"):
        input("What is the first vehicle located at " + address + "?")


def scrape_Tax_Commitment_Book():
    from PyPDF2 import PdfReader
    import json

    reader = PdfReader("Forms/FY2021 RE Tax Commitment Book.pdf")

    # print(reader.pages)

    return_dict = {

    }

    x = 1
    total_length = len(reader.pages)

    print(total_length)

    for i in range(len(reader.pages)):
        page = reader.pages[int(i)].extract_text().split("\n")

        # print(page)
        # cat = list(page)

        # print(cat[6][:cat[6].index("|")].strip())
        # print(cat[7][:cat[7].index("|")].strip())
        try:
            owner1 = list(page)[6][:list(page)[6].index("|")].strip()
            owner2 = list(page)[7][:list(page)[6].index("|")].strip()
            owner3 = list(page)[17][:list(page)[6].index("|")].strip()
            owner4 = list(page)[18][:list(page)[6].index("|")].strip()
            owner5 = list(page)[28][:list(page)[6].index("|")].strip()
            owner6 = list(page)[29][:list(page)[6].index("|")].strip()
            owner7 = list(page)[39][:list(page)[6].index("|")].strip()
            owner8 = list(page)[40][:list(page)[6].index("|")].strip()

            # print("Owner 1:" + owner1)
            # print("Owner 2:" + owner2)
            # print("Owner 3:" + owner3)
            # print("Owner 4:" + owner4)
            # print("Owner 5:" + owner5)
            # print("Owner 6:" + owner6)
            # print("Owner 7:" + owner7)
            # print("Owner 8:" + owner8)

            address1 = list(page)[11][5:list(page)[6].index("|")].strip()
            address2 = list(page)[22][5:list(page)[6].index("|")].strip()
            address3 = list(page)[33][5:list(page)[6].index("|")].strip()
            address4 = list(page)[44][5:list(page)[6].index("|")].strip()

            # print("Address1: " + address1)
            # print("Address2: " + address2)
            # print("Address3: " + address3)
            # print("Address4: " + address4)

            return_dict[address1] = [owner1, owner2]
            return_dict[address2] = [owner3, owner4]
            return_dict[address3] = [owner5, owner6]
            return_dict[address4] = [owner7, owner8]
        except:
            pass
        # 6,7,17,18,28,29

        # for result in page:
        #
        #    if "|Building" in result:
        #
        #        owner = result.split("|")[0]
        #
        #
        #        print("Owner: " + owner)
        #
        #
        #
        #    if "LOC: " in result:
        #        address = result[5:result.index("|")].strip()
        #        # print(address)
        #        # return_dict["Address"].append(address)
        #
        #        print("Address: " + address)
        #
        #        return_dict[address] = owner
        #
        #
        print(str(x) + ":" + str(total_length))
        x += 1
    print(return_dict)
    with open("C:\\Users\Don\AppData\Roaming\JetBrains\PyCharm2020.2\scratches\\test123.json", "w") as outfile:
        json.dump(return_dict, outfile)


def address_To_Lat_Long():
    import requests, json, googlemaps
    from datetime import datetime

    with open("C:\\Users\Don\AppData\Roaming\JetBrains\PyCharm2020.2\scratches\\test123.json") as infile:
        data = json.load(infile)

    for i, value in data.items():
        gmaps = googlemaps.Client(key='AIzaSyAnRJvIU0LM1tPQCKgBZntZJn04ukyvp5o')
        geocode_result = gmaps.geocode(i + ", Billerica, MA")
        print(str(geocode_result[0]["geometry"]["location"]["lat"]) + "," + str(
            geocode_result[0]["geometry"]["location"]["lng"]))

    # return geocode_result


def facebook_OCR():
    from PIL import Image
    import pytesseract

    print(pytesseract.image_to_string(Image.open('test.png')))


def scrape_Billerica_Budget_PDF():
    import PyPDF2
    import json

    pages_to_scrape = {"Administration": 203}
    # ,
    # ,
    # ",
    # "Fire Department": 188,
    # "Accounting": 52}

    pdf = open("Forms/2025 Billerica Budget.pdf", "rb")
    reader = PyPDF2.PdfReader(pdf)

    police_dict = {}

    for department, page_num in pages_to_scrape.items():

        page = reader.pages[page_num]

        page_text = page.extract_text().split("\n")

        for row in page_text:
            print(row)

            cat = row.strip("\n").split(" ")
            print(cat)

            try:
                print("Attempting to add: " + cat[0] + " " + cat[1])
                police_dict[cat[0] + " " + cat[1]] = {"Rank": cat[2],
                                                      "Seniority": cat[3],
                                                      "Anniversary Date": cat[4]}

                print("{0} {1} was added successfully!".format(cat[0], cat[1]))

            # print(text)
            except IndexError:
                print("Skipping: " + cat[0] + " " + cat[1])
            print(police_dict)


    with open(
            "C:\\Users\Don\Documents\Github Folder\\Ultimate-Security-Software\Forms\Billerica Employee Records\\Administration Roster.json",
            "w") as outfile:
        json.dump(police_dict, outfile)


#return_dict = {}
#with open("Forms/Billerica Employee Records/State Police Roster.csv", "r") as csv_file:
#    for line in csv_file:
#        line_data = line.replace("\n","").split(",")
#
#        print(line_data[2] +" " + line_data[3])
#
#        return_dict[line_data[2] +" " + line_data[3]] = {
#            "Rank": line_data[5],
#            "Department Zip": line_data[23],
#        }
#import json
#
#
#with open('result.json', 'w') as fp:
#    json.dump(return_dict, fp)