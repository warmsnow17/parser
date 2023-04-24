import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import csv
import time
from dotenv import load_dotenv
load_dotenv()


timestr = time.strftime("%Y%m%d-%H%M%S")

with webdriver.Chrome() as browser:
    browser.get(os.getenv('URL_SITE'))
    browser.set_window_size(1024, 720)
    field = browser.find_elements(By.CLASS_NAME, 'LandingFormGroup__input___IzEIT')
    field[0].send_keys(os.getenv('EMAIL'))
    time.sleep(.5)
    field[1].send_keys(os.getenv('PASSWORD'))
    time.sleep(.5)
    browser.find_element(By.TAG_NAME, 'button').click()
    time.sleep(10)
    with open(f'{timestr}.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Рубрика', 'Название', 'Фирма', 'Контакты1', 'Контакты2', 'Контакты3', 'Контакты4', 'Контакты5'
        ])
        find_names_of_parts = browser.find_elements(By.CLASS_NAME, 'SidebarKeysList__keyText___wDHFL.clipped-text')
        names_of_parts = [x.text for x in find_names_of_parts]
        buttons_of_groups = browser.find_elements(
            By.CLASS_NAME,
            'SidebarKeysList__value___2-sq9',
        )
        for i_group in range(0, 5):
            buttons_of_groups[i_group].click()
            time.sleep(.5)
            for i_scroll in range(13):
                ActionChains(browser).scroll(280, 300, 280, 800).perform()
                time.sleep(2)
                orders = browser.find_elements(
                    By.CLASS_NAME,
                    'TenderPlate__plate___3Vo8p.flex-justify-center.flex-column'
                )
                for i in range(len(orders)):
                    try:
                        orders[i].click()
                        time.sleep(1)
                        name_of_order = browser.find_element(By.CLASS_NAME, 'TenderHeader__tenderName__inner___3QrlF')
                    except:
                        continue
                    try:
                        name_of_firm_customer = browser.find_element(
                            By.CLASS_NAME,
                            'TenderModel__customerLink___24a3L.TenderModel__severalCustomersLink___2echE'
                        ).text
                        time.sleep(.5)
                    except:
                        name_of_firm_customer = 'Не удалось записать название фирмы'
                    contacts_info = browser.find_elements(By.TAG_NAME, 'td')
                    text_contacts_info = [x.text for x in contacts_info]
                    try:
                        first_info = text_contacts_info[1].split('\n')[0]
                    except:
                        first_info = '---'
                    try:
                        second_info = text_contacts_info[1].split('\n')[1]
                    except:
                        second_info = '---'
                    try:
                        third_info = text_contacts_info[1].split('\n')[2]
                    except:
                        third_info = '---'
                    try:
                        fourth_info = text_contacts_info[1].split('\n')[3]
                    except:
                        fourth_info = '---'
                    try:
                        fifth_info = text_contacts_info[1].split('\n')[4]
                    except:
                        fifth_info = '---'
                    new_row = names_of_parts[i_group], \
                              name_of_order.text, \
                              name_of_firm_customer, \
                              first_info, \
                              second_info, \
                              third_info, \
                              fourth_info, \
                              fifth_info
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(new_row)

