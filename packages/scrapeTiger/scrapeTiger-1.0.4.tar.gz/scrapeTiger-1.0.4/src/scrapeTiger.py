from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


link_list = []
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def multi_page(url,start_page,end_page,css_selector,wait_second=2): 
    url = url
    for page_num in range(start_page,end_page):
        driver.get(url+f'{page_num}')
        page_url =(url+f'{page_num}')
        print('page_url: ',page_url)
        time.sleep(wait_second)
        
        try:
            box = driver.find_elements(By.CSS_SELECTOR,css_selector)
        except:
            print("Invalid css selector")
            
        for i in box:
            product_link = i.get_attribute("href")
            print(product_link )
            link_list.append(product_link)

def single_page(url,css_selector,wait_second=2):
    url = url
    print('page_url',url)
    driver.get(url)
    time.sleep(wait_second)
    try:
       box = driver.find_elements(By.CSS_SELECTOR,css_selector)
    except:
        print("Invalid css selector")
    for i in box:
            product_link = i.get_attribute("href")
            print(product_link)
            link_list.append(product_link)

         
def details_page(wait_second=2,field_one_css=None,field_one_html=False,field_two_css=None,field_two_html=False,field_three=None,field_three_html = False,field_four=None,field_four_html=False,main_image_css=None,img_attribute='src',gallary_image_css=None,gallary_image_attribute='src',header_added=False):
    for i in link_list:
        url = i
        driver.get(i)
        time.sleep(wait_second)
        try:
            if field_one_html == False:
                field_one = driver.find_element(By.CSS_SELECTOR,field_one_css).text
                print('field_one: ',field_one)
            if field_one_html == True:
                field_one = driver.find_element(By.CSS_SELECTOR,field_one_css)
                field_one = field_one.get_attribute("innerHTML")
                print('field_one: ',field_one)
        except:
            field_one = None
            print("field_one_css not set")

        try:
            if field_two_html == False:
                field_two = driver.find_element(By.CSS_SELECTOR,field_two_css).text
                print('field_two: ',field_two)
            if field_two_html == True:
                field_two = driver.find_element(By.CSS_SELECTOR,field_two_css)
                field_two = field_two.get_attribute("innerHTML")
                print('field_two: ',field_two)
        except:
            field_two = None
            print("field_two_css not set")

        try:
            if field_three_html == False:
                field_three = driver.find_element(By.CSS_SELECTOR,field_three_css).text
                print('field_three: ',field_three)
            if field_three_html == True:
                field_three = driver.find_element(By.CSS_SELECTOR,field_three_css)
                field_three = field_two.get_attribute("innerHTML")
                print('field_three: ',field_three)
        except:
            field_three = None
            print("field_three_css not set")

        try:
            if field_four_html == False:
                field_four = driver.find_element(By.CSS_SELECTOR,field_four_css).text
                print('field_four: ',field_four)
            if field_four_html == True:
                field_four = driver.find_element(By.CSS_SELECTOR,field_four_css)
                field_four = field_four.get_attribute("innerHTML")
                print('field_four: ',field_four)
        except:
            field_four = None
            print("field_four_css not set")

        try:
            main_image = driver.find_element(By.CSS_SELECTOR,main_image_css)
            main_image = main_image.get_attribute(img_attribute)
            print("main_image: ",main_image)
        except:
            main_image = None
            print("main_image_css not set")

        try:
            gallary_images_list = []
            gallary_images = driver.find_elements(By.CSS_SELECTOR,gallary_image_css)
            for i in gallary_images:
                    gallary_image = i.get_attribute(gallary_image_attribute)
                    gallary_images_list.append(gallary_image)
                    print('gallary_image: ',gallary_image)
        except:
            gallary_images = None
            print("gallary_image_css not set")
        
        with open("scraping.csv", "a", encoding="utf-8", newline='') as f:
                writeFile = csv.writer(f)
                if not header_added:
                   header = ['url','field_one','field_two','field_three','field_four','main_image','gallary_images_list']
                   writeFile.writerow(header)
                   header_added = True
                writeFile.writerow([url,field_one,field_two,field_three,field_four,main_image,gallary_images_list])
        gallary_images_list.clear()
            

        
 
