from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException,TimeoutException
import time
import csv

driver=webdriver.Chrome(service=chromeService(ChromeDriverManager().install()))

url="https://www.timeanddate.com/weather/"

def retry_delay(driver,url,max_attempts=3):
    for attempt in range(1, max_attempts+1):
        try:
            driver.get(url)
            return True
        except (TimeoutException,WebDriverException) as e:
            if attempt< max_attempts:
                wait=2 * attempt
                time.sleep(wait)
            else:
                print(f"Giving up on url: {url} because of :{e}")
                return False


retry_delay(driver,url)
regions = ("Africa", "Asia", "Australia", "Capitals", "Europe", "North America", "South America")

continents=driver.find_elements(By.XPATH,"//li[@class='tad-link-list-item']//a")
continent_urls=[]
for c in continents:
    continent_urls.append(c.get_attribute("href"))

for link,region in zip(continent_urls,regions):
    retry_delay(driver,link)
    continent_country_list=[]
    rows=driver.find_elements(By.XPATH,"//tr[td[contains(@class,'tad-weather-table__city-cell')]/a]")
    for r in rows:
        city=r.find_element(By.CSS_SELECTOR,'td.tad-weather-table__city-cell a').text
        country=r.find_element(By.CSS_SELECTOR,'td.tad-weather-table__country-cell').text
        temperature_element=r.find_elements(By.CSS_SELECTOR,'td.tad-weather-table__temperature-cell')
        if temperature_element:
            temperature = temperature_element[0].text
        else:
            temperature = ""
        wind_element=r.find_elements(By.CSS_SELECTOR,'td.tad-weather-table__wind-cell div.tad-weather-table__wind-cell-inner')
        if wind_element:
            wind=wind_element[0].text
        else:
            wind=""
        weather_dic={}
        weather_dic["City"]=city
        weather_dic["Country"]=country
        weather_dic["Temperature"]=temperature
        weather_dic["Wind"]=wind
        continent_country_list.append(weather_dic)
    
    with open(f"{region}.csv","w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file, fieldnames=["City","Country","Temperature","Wind"])
        writer.writeheader()
        writer.writerows(continent_country_list)


driver.quit()
