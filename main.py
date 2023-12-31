import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import io


with open('secret.json') as config_file:
    config_data = json.load(config_file)

password = config_data['credentials']['password']


def upload_to_Gdrive(name,image_url,password):
    headers = {"Authorization": password}
    para = {
        "name": name,
        "parents": ["1MNo4lJMavozY5VLhF2oJzSY5YgoeJoBz"]
    }
    files = {
        "data": ('metadata',json.dumps(para), 'application/json; charset=UTF-8'),
        "file": io.BytesIO(requests.get(image_url).content)
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers = headers,
        files = files)
    print("Response Status Code:", r.status_code)
    print("Response Content:", r.content.decode())
    print("Uploaded: ", image_url)



def scrape_data():
    driver = webdriver.Chrome(executable_path='/Users/jiawenng/Desktop/drivers/chromedriver')
    base_url = "https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge"
    driver.get(base_url)
    wait = WebDriverWait(driver, 220)
    lastpage = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'page-count')))
    #lastpagenum = int(lastpage.text)
    lastpagenum = 10

    for page_num in range(1, lastpagenum+1):
        current_url = f"{base_url}?pageNumber={page_num}"

        driver.get(current_url)
        wait = WebDriverWait(driver, 220)
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-tile-v2')))

        product_links = [product.get_attribute("href") for product in wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-title-link.ng-star-inserted")))]

        for product_link in product_links:
            driver.get(product_link)
            additional_images = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'thumbnail-image')))
            product_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'shelfProductTile-title'))).text
            pic_index = 0
            for additional_image in additional_images:
                pic_index = pic_index + 1
                image_url = additional_image.get_attribute('src')
                image_title = product_title + ' ' + str(pic_index)
                print(image_url)
                print(image_title)

                upload_to_Gdrive(image_title, image_url, password)




        # for product in products:
        #     title = product.find_element_by_css_selector('.product-title-link.ng-star-inserted').text
        #     image = product.find_element_by_css_selector('.product-tile-v2--image img').get_attribute('src')
        #     title_element = product.find_element_by_css_selector('.product-title-link.ng-star-inserted')
        #     print(title)
        #     print(image)
        #     print(page_num)
        #     # upload_to_Gdrive(title, image, password)
        #


    driver.quit()


# def retrieve_from_Gdrive():




if __name__ == '__main__':
    # upload_to_Gdrive('jwpicture.png','https://i.natgeofe.com/n/4f5aaece-3300-41a4-b2a8-ed2708a0a27c/domestic-dog_thumb_16x9.jpg?w=1200',password)
    scrape_data()

