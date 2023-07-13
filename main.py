import time
import requests
import lxml
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
link = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.847305285867%2C%22east%22%3A-122.31488314990234%2C%22south%22%3A37.70320840844272%2C%22west%22%3A-122.55177585009766%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A390355%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A2000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"
# link = input("Paste the link of the item you want to track the price of: ")
response = requests.get(url=f'{link}', headers=headers)


#beautiful soup to extract data
data = response.text
soup = BeautifulSoup(data, "lxml")
price_list = []

#for getting prices
price = soup.find_all('span',  class_= 'PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1')

for each_price in price:
    price_value = each_price.get_text().strip()

    # Remove the "$" symbol
    price_without_dollar = price_value.replace("$", "")

    # Remove "/mo"
    price_cleaned = price_without_dollar.replace("/mo", "")
    price_without_add = price_cleaned.split('+')[0]
    final_price = int(price_without_add.replace(",", ""))

    price_list.append(final_price)

print(price_list)

#For getting Addresses
address_list = []
link_list = []

address= soup.find_all('a',  class_= 'StyledPropertyCardDataArea-c11n-8-89-0__sc-yipmu-0')

for each_address in address:
    address_value = each_address.get_text().strip()
    link = each_address['href']

    address_list.append(address_value)
    link_list.append(link)


print(address_list)
print(link_list)
complete_links=[]

# To fill in all the incomplete links


for link in link_list:
    if link.startswith("https://"):
        complete_links.append(link)

    else:
        complete_links.append("https://www.zillow.com" + link)


print(complete_links)


#PASSING THIS DETAILS TO THE FORM

chrome_driver_path = "/Users/dona/Documents/chromedriver"
chrome_options = Options()
chrome_options.location = chrome_driver_path
driver = webdriver.Chrome(options=chrome_options)


for i in range(len(price_list)):
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSelv2v31a-lURMHRo4HWnRT9Agu_sd1rPy1h5AHyyMkImegPw/viewform?usp=sf_link')
    price_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_form = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea')
    link_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    nowprice = price_list[i]
    price_form.send_keys(nowprice)
    nowaddress = address_list[i]
    address_form.send_keys(nowaddress)
    nowlink = complete_links[i]
    link_form.send_keys(nowlink)
    i = i + 1
    time.sleep(2)
    submitbtn = driver.find_element(By.CLASS_NAME, 'NPEfkd')
    submitbtn.click()
    time.sleep(2)
    another_response = driver.find_element(By.CSS_SELECTOR, '.c2gzEf a')
    another_response.click()
    time.sleep(2)


driver.quit()






