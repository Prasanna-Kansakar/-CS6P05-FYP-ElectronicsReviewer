from re import A    
import time
from unicodedata import name
from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from proj import settings

from bs4 import BeautifulSoup as soup
from selenium import webdriver
#import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from .models import Accessories05Price, Bookmark01Laptop_Bookmark, Bookmark02Accessories_Bookmark, Laptop01Laptop, Laptop10Price

@shared_task(bind=True)
def LaptopScraping(self):
    upd = Laptop10Price.objects.filter(type=2)
    for item  in upd:
        item.is_updated = False
        item.save()
    ser = Service("D:\chromedriver")
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    op.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(service=ser, options=op)
    baseurl = 'https://www.sastodeal.com/electronic/laptops.html?p=1'
    driver.get(baseurl)
    page = driver.execute_script("return document.documentElement.outerHTML")
    pg_soup = soup(page, "lxml")
    page_no = pg_soup.find('ul', {"class": "items pages-items"}).findAll('li')
    l = page_no[len(page_no) - 2].a.text.split(" ")
    n= int(l[1])+1
    n=5
    for i in range (1,n):
        new_url = f'https://www.sastodeal.com/electronic/laptops.html?p={i}'
        driver.get(new_url)
        page = driver.execute_script("return document.documentElement.outerHTML")
        pg_soup = soup(page, "lxml")
        items = pg_soup.findAll('li', {"class": "item product product-item"})
        for item in items:
            class1 = item.find('div', {"class": "product details product-item-details"})
            title = class1.a.text
            Url = class1.a['href']
            class2 = class1.find('div', {"class": "price-box price-final_price"})
            try:
                x = class2.find('span', {'class': 'old-price priceold-line'}).text.split(" ")
                x = list(filter(None, x))
                Price = float(x[len(x)-2].replace(',', ''))
                x = class2.find('span', {'class': 'special-price pricenew'}).text.split(" ")
                x = list(filter(None, x))
                Discount_price = float(x[len(x)-2].replace(',', ''))
                discount = True
            except:
                x = class2.find('span', {'class': 'price'}).text.split(" ")
                x = list(filter(None, x))
                Price = float(x[len(x)-1].replace(',', ''))
                Discount_price = 0
                discount = False
            check = Laptop10Price.objects.filter(url=Url)
            if check.exists():
                obj = check.first()
                obj.price = Price
                obj.discount_price = Discount_price
                obj.has_discount = discount
                obj.type=2 
                obj.is_updated=True          
                obj.save()
            else:
                obj = Laptop10Price(name=title, url=Url, price = Price, discount_price = Discount_price, has_discount = discount, is_updated=True , type=2)
                obj.save()
    items = Laptop10Price.objects.filter(type=2,is_deleted=False)
    for item in items:
        if not item.is_updated:
            item.is_deleted = True
            item.save()
    driver.quit()

@shared_task(bind=True)
def LaptopScraping2(self):
    upd = Laptop10Price.objects.filter(type=1)
    for item  in upd:
        item.is_updated = False
        item.save()
    ser = Service("D:\chromedriver")
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    op.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(service=ser, options=op)
    baseurl = 'https://www.daraz.com.np/laptops/?page=1&spm=a2a0e.11779170.cate_1.4.287d2d2bvhIt5Y'
    driver.get(baseurl)
    page = driver.execute_script("return document.documentElement.outerHTML")

    pg_soup = soup(page, "lxml")

    page_no = pg_soup.find('ul', {"class": "ant-pagination"}).findAll('li')
    l = int(page_no[len(page_no) - 2].a.text) + 1
    for i in range(1, l):
        new_url = f'https://www.daraz.com.np/laptops/?page={i}&spm=a2a0e.11779170.cate_1.4.287d2d2bvhIt5Y'
        driver.get(new_url)
        page = driver.execute_script("return document.documentElement.outerHTML")
        pg_soup = soup(page, "lxml")
        items = pg_soup.findAll('div', {"class": "c2prKC"})
        for i in range(1, l):
            new_url = f'https://www.daraz.com.np/laptops/?page={i}&spm=a2a0e.11779170.cate_1.4.287d2d2bvhIt5Y'
            driver.get(new_url)
            page = driver.execute_script("return document.documentElement.outerHTML")
            pg_soup = soup(page, "lxml")
            items = pg_soup.findAll('div', {"class": "box--pRqdD"})
            for item in items:
                class1 = item.find('div', {"class": "info--ifj7U"})
                Url = "https:" + class1.a['href']
                title = class1.a.text
                class3 = item.find('div', {"class": "price--NVB62"})
                class4 = item.find('div', {"class": "priceExtra--ocAYk"})
                try:
                    x = class4.find('span').text.split(" ")
                    Price = int(x[len(x) - 1].replace(',', ''))
                    x = class3.find('span').text.split(" ")
                    Discount_price = int(x[len(x) - 1].replace(',', ''))
                    discount = True
                except:
                    x = class3.find('span').text.split(" ")
                    Price = int(x[len(x) - 1].replace(',', ''))
                    Discount_price = 0
                    discount = False
            check = Laptop10Price.objects.filter(url=Url)
            if check.exists():
                obj = check.first()
                obj.price = Price
                obj.discount_price = Discount_price
                obj.has_discount = discount
                obj.type=1 
                obj.is_updated=True          
                obj.save()
            else:
                obj = Laptop10Price(name=title, url=Url, price = Price, discount_price = Discount_price, has_discount = discount, is_updated=True , type=1)
                obj.save()

    items = Laptop10Price.objects.filter(type=1,is_deleted=False)
    for item in items:
        if not item.is_updated:
            item.is_deleted = True
            item.save()
    driver.quit()

@shared_task(bind=True)
def AccessoryScraping(self):
    upd = Accessories05Price.objects.all()
    for item  in upd:
        item.is_updated = False
        item.save()
    ser = Service("D:\chromedriver")
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    op.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(service=ser, options=op)
    baseurl = 'https://www.sastodeal.com/electronic/computer-laptop-peripherals/mouse.html?p=1'
    driver.get(baseurl)
    page = driver.execute_script("return document.documentElement.outerHTML")
    pg_soup = soup(page, "lxml")
    page_no = pg_soup.find('ul', {"class": "items pages-items"}).findAll('li')
    l = page_no[len(page_no) - 2].a.text.split(" ")
    n=0
    for i in range (1,int(l[1])+1):
        new_url = f'https://www.sastodeal.com/electronic/computer-laptop-peripherals/mouse.html?p={i}'
        driver.get(new_url)
        page = driver.execute_script("return document.documentElement.outerHTML")
        pg_soup = soup(page, "lxml")
        items = pg_soup.findAll('li', {"class": "item product product-item"})
        for item in items:
            class1 = item.find('div', {"class": "product details product-item-details"})
            title = class1.a.text
            Url = class1.a['href']
            class2 = class1.find('div', {"class": "price-box price-final_price"})
            try:
                x = class2.find('span', {'class': 'old-price priceold-line'}).text.split(" ")
                Price = float(x[len(x)-2].replace(',', ''))
                x = class2.find('span', {'class': 'special-price pricenew'}).text.split(" ")
                Discount_price = float(x[len(x)-2].replace(',', ''))
                discount = True
            except:
                x = class2.find('span', {'class': 'price'}).text.split(" ")
                Price = float(x[len(x)-1].replace(',', ''))
                Discount_price = 0
                discount = False
            check = Accessories05Price.objects.filter(url=Url)
            if check.exists():
                obj = check.first()
                obj.price = Price
                obj.discount_price = Discount_price
                obj.has_discount = discount
                obj.type=2
                obj.is_updated=True          
                obj.save()
            else:
                obj = Accessories05Price(name=title, url=Url, price = Price, discount_price = Discount_price, has_discount = discount, is_updated=True , type=2)
                obj.save()
    baseurl = 'https://www.sastodeal.com/electronic/computer-laptop-peripherals/keyboards.html?p=1'
    driver.get(baseurl)
    page = driver.execute_script("return document.documentElement.outerHTML")
    pg_soup = soup(page, "lxml")
    page_no = pg_soup.find('ul', {"class": "items pages-items"}).findAll('li')
    l = page_no[len(page_no) - 2].a.text.split(" ")
    n=0
    for i in range (1,int(l[1])+1):
        new_url = f'https://www.sastodeal.com/electronic/computer-laptop-peripherals/keyboards.html?p={i}'
        driver.get(new_url)
        page = driver.execute_script("return document.documentElement.outerHTML")
        pg_soup = soup(page, "lxml")
        items = pg_soup.findAll('li', {"class": "item product product-item"})
        for item in items:
            image = item.find('img', {"class": "product-image-photo"})
            Img_url = image['src']
            class1 = item.find('div', {"class": "product details product-item-details"})
            title = class1.a.text
            Url = class1.a['href']
            class2 = class1.find('div', {"class": "price-box price-final_price"})
            try:
                x = class2.find('span', {'class': 'old-price priceold-line'}).text.split(" ")
                Price = float(x[len(x)-2].replace(',', ''))
                x = class2.find('span', {'class': 'special-price pricenew'}).text.split(" ")
                Discount_price = float(x[len(x)-2].replace(',', ''))
                discount = True
            except:
                x = class2.find('span', {'class': 'price'}).text.split(" ")
                Price = float(x[len(x)-1].replace(',', ''))
                Discount_price = 0
                discount = False
            check = Accessories05Price.objects.filter(url=Url)
            if check.exists():
                obj = check.first()
                obj.price = Price
                obj.discount_price = Discount_price
                obj.has_discount = discount
                obj.img_url=Img_url
                obj.type=2 
                obj.is_updated=True          
                obj.save()
            else:
                obj = Accessories05Price(name=title, url=Url, price = Price, discount_price = Discount_price, has_discount = discount,img_url=Img_url, is_updated=True , type=2)
                obj.save()
    items = Accessories05Price.objects.filter(is_deleted=False)
    for item in items:
        if not item.is_updated:
            item.is_deleted = True
            item.save()
    driver.quit()


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    for user in users:
        send = False
        Format = "{0}(Original Price = {1} Discount Price = {2}): \n Link: {3}\n"
        mail_subject = "Following items are avialable on Sale:"
        laptops = Bookmark01Laptop_Bookmark.objects.filter(user=user)
        accessories = Bookmark02Accessories_Bookmark.objects.filter(user=user)
        message = "The following items you have bookmarked are on sale: \n"
        to_email = user.email
        for laptop in laptops:
            obj = laptop.laptop
            items = obj.prices.filter(has_discount=True)
            for item in items:
                message += Format.format(item.name, item.price, item.discount_price, item.url)
                send = True
        for accessory in accessories:
            obj = accessory.accessory
            items = obj.prices.filter(has_discount=True)
            for item in items:
                message += Format.format(item.name, item.price, item.discount_price, item.url)
                send = True
        if send:
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
    return "Done"