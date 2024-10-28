import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class MonitorScraper:
    def __init__(self,
                 headless= True,
                 load_images = False,
                 chromedriver_path = "./chromedriver",
                 window_size=(700,900),
    ):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-gpu-compositing")
            options.add_argument("--log-level=3") 

        if not load_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs",prefs)
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.driver.set_window_size(*window_size)

    def scrape_amazon(self, search_url):
        self.driver.get(search_url)


        try:
            WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,'/html/body/div[1]/span/form/div[2]/span[2]/span/button')))
            amazon_reject_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/span/form/div[2]/span[2]/span/button')
            amazon_reject_button.click()
        except Exception as e:
            print(f"No reject button found to click {e}")
        


        products_data = []
        
        product_elements = self.driver.find_elements(By.CSS_SELECTOR,".s-main-slot .s-result-item")

        for product in product_elements:

            try:
                product_name = product.find_element(By.CSS_SELECTOR,'span.a-text-normal').text
            except:
                product_name = "N/A"

            try:
                price_whole = product.find_element(By.CLASS_NAME,'a-price-whole').text
                price_fraction = product.find_element(By.CLASS_NAME,'a-price-fraction').text
                price = f"{price_whole}.{price_fraction} €"
            except:
                price = "N/A"

            try:
                product_url = product.find_element(By.CSS_SELECTOR,'a.a-link-normal').get_attribute('href')
            except:
                product_url = "N/A"
            
            
            products_data.append([product_name,price,product_url])

        df = pd.DataFrame(products_data,columns=["Product Name","Price","URL"])
        return df
    def scrape_otto(self,search_url):
        self.driver.get(search_url)

        try:
            WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]')))
            otto_reject_button = self.driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/button[2]')
            otto_reject_button.click()
        except Exception as e:
            print(f"No Reject button found to click {e}")

        products_data = []
        product_elements = self.driver.find_elements(By.CLASS_NAME,'product-item')

        for product in product_elements:
            try:
                product_name = product.find_element(By.CLASS_NAME,'product-title').text
            except Exception as e:
                product_name = "N/A"
                print(f"Error while pulling the product name: {e}")
            
            try:
                price= product.find_element(By.CLASS_NAME,'price').text
            except Exception as e:
                price = "N/A"
                print(f"Error while pulling the price: {e}")
            
            try:
                product_url = product.find_element(By.TAG_NAME,'a').get_attribute('href')
            except Exception as e:
                product_url = "N/A"
                print(f"Error while getting the product url: {e}")
            
            products_data.append([product_name, price, product_url])
        
        return pd.DataFrame(products_data, columns=["Product Name", "Price", "URL"])
    
    def scrape_saturn(self, search_url):
        self.driver.get(search_url)

        try:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[2]/div/form/div[2]/button[1]')))
            saturn_reject_button = self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/form/div[2]/button[1]')
            saturn_reject_button.click()
        except Exception as e:
            print(f"No reject button found: {e}")
        
        products_data = []
        products_elements = self.driver.find_elements(By.CLASS_NAME,'product-item')

        for product in products_elements:
            try:
                product_name = product.find_element(By.CLASS_NAME,'product-title').text
            except Exception as e:
                product_name = "N/A"
                print(f"Error while getting the product name: {e}")
            
            try:
                price = product.find_element(By.CLASS_NAME,'price').text
            except Exception as e:
                price = "N/A"
                print(f"Error while getting price: {e}")
            
            try:
                product_url = product.find_element(By.TAG_NAME,'a').get_attribute('href')
            except Exception as e:
                product_url = "N/A"
                print(f"Error while getting product url: {e}")
            
            products_data.append([product_name, price,product_url])
        
        return pd.DataFrame(products_data, columns=["Product Name", "Price", "URL"])
    

    def scrape_all(self):
        try:
            amazon_data = self.scrape_amazon('https://www.amazon.de/s?k=monitors')
            otto_data = self.scrape_otto('https://www.otto.de/suche/?q=monitors')
            saturn_data = self.scrape_saturn('https://www.saturn.de/de/search.html?query=monitors')


            all_data = pd.concat([amazon_data,otto_data,saturn_data], ignore_index=True)
            return all_data
        finally:
            self.driver.quit()
