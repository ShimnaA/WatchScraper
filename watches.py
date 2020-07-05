from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dataclasses import dataclass

import time

@dataclass
class Brand:
    label: str
    link: str
    watchcount: int

class WatchScraper:
    def __init__(self, ):
        self.base_url = "https://www.ethoswatches.com/brands.html"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(50)  # Set impicit waits for 50 seconds

    def get_brands(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        brands = soup.find(class_='items am_shopby_filter_items_attr_manufacturer')
        brands = brands.find_all(class_='item')
        brand_list = []
        for brand in brands:
            link = brand.find('a').get('href')
            label = brand.get_text()
            label_count_list = label[3:].split('\n')
            label = label_count_list[0]
            watchcount = int(label_count_list[1])
            brand_list.append(Brand(label, link, watchcount))
        print(brand_list)


    def main_logic(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.get_brands()



        time.sleep(3)
        self.driver.quit()

if __name__ == '__main__':
    watch_details = WatchScraper()
    watch_details.main_logic()