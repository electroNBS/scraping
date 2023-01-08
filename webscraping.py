from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
import requests

headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planet_data = []

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("D:\Personal\Coding\WHjr\python\C127\C127Class\venv\chromedriver_win32\chromedriver.exe")
browser.get(start_url)

time.sleep(10)

def scrap():
    
    
    for i in range(0,210):
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        currentpgno=int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
        if currentpgno < i:
            next = browser.find_element(by = By.XPATH, value = "/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a")
            next.click()
            
        elif currentpgno > i:
            back = browser.find_element(by = By.XPATH, value = "/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a")
            back.click()
            
        else:
            break
        
        for ul_tag in soup.find_all("ul", attrs={"class","exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(ul_tag):
                if index ==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
                        
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov/"+ hyperlink_li_tag.find_all("a", href = True)[0]["href"])
            
            
            planet_data.append(temp_list)
            
        next = browser.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/footer/div/div/div/nav/span[2]/a")
        next.click()
        print(f"page {i} scrapping done")
        
scrap()

new_planet_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs = {"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                    
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
        
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        
for index,data in enumerate(planet_data):
    scrape_more_data(data[5])
    print(f"scrapping hyperlink {index+1} done")

final_planet_data = []

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [item.replace("\n","")for item in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)
    
with open("scrapper2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)

