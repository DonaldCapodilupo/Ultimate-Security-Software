with open("api-key.txt", "r") as file:
    key = file.read()


def scrape_Google_Maps_Long_Lat():
    import pyperclip, csv

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

    with open("static/Property Reports/" + street_num + " " + street_name + ".html", "w", encoding='utf-8') as f:
        f.write(pyperclip.paste())

    driver.close()

    # Used for mass scraping


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
            offense_text = item[: item.index("Name:")].replace("   "," ").replace("_","")

            name_text = item[item.index("Name:"): item.index("Age:")].replace("   "," ")[6:].strip()

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