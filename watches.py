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
        self.brand_list = []


    def get_brands(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        brands = soup.find(class_='items am_shopby_filter_items_attr_manufacturer')
        brands = brands.find_all(class_='item')

        for brand in brands:
            link = brand.find('a').get('href')
            label = brand.get_text()
            label_count_list = label[3:].split('\n')
            label = label_count_list[0]
            watchcount = int(label_count_list[1])
            self.brand_list.append(Brand(label, link, watchcount))
        print(self.brand_list)

    def get_productlist(self,brandlink):
        self.driver.get(brandlink)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        watchlist1 = soup.find(class_='columns')
        watchlist_soup = watchlist1.div.find_all('li')
        product_list = []
        for watch in watchlist_soup:
            if watch.find('h2') is not None:
                link = watch.find('a').get('href')
                product_list.append(link)
        return product_list

    def get_watchdetails(self,product_list):
        for product_link in product_list:
            print(product_link)
            self.driver.get(product_link)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            product_info = soup.find(class_='product_info_main')

            print(product_info.h1.span.text.strip())
            print(product_info.h3.text.strip())
            print(product_info.find(class_='price').text)
            print(product_info.find(class_='product_emi').text.strip())
            image_info = soup.find(class_='openPhotoSwipe').findChildren("img")
            image_info_tag = image_info[0]["alt"]
            image_info_src = image_info[0]["src"]
            print(image_info_tag)
            print(image_info_src)

    def main_logic(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.get_brands()
        for brand in self.brand_list:
            product_list = self.get_productlist(brand.link)
            self.get_watchdetails(product_list)



        time.sleep(3)
        self.driver.quit()

if __name__ == '__main__':
    watch_details = WatchScraper()
    watch_details.main_logic()