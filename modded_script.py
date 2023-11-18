import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = "/Users/macbook/Downloads/chromedriver"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=cats&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            soup = BeautifulSoup(wd.page_source, 'html.parser')
            images = soup.find_all('img', {'class': 'n3VNCb'})

            for image in images:
                src = image.get('src')
                if src and 'http' in src:
                    image_urls.add(src)
                    print(f"Found {len(image_urls)}")

    return image_urls

def download_image(download_path, url, file_name):
    try:
        response = requests.get(url, stream=True)
        image = Image.open(io.BytesIO(response.content))
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

# Create 'imgs' folder if it doesn't exist
if not os.path.exists("imgs"):
    os.makedirs("imgs")

urls = get_images_from_google(wd, 1, 10)

for i, url in enumerate(urls):
    download_image("/Users/macbook/Desktop/Personal Projects/Selenium-Image-Scraping/imgs", url, f"{i + 1}.jpg")

wd.quit()
