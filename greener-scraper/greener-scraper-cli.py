import os
import sys
import time
from functools import partial
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920,1080')
chrome_options.add_argument('start-maximised')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def scroll_to_page_end_n_times(browser, s, page_load_wait_seconds):
  for _ in range(s):
    print(f'ScrollHeight before scrolling: {browser.execute_script("return document.documentElement.scrollHeight")}')
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    print(f'Scrolled, waiting for {page_load_wait_seconds} seconds to load page')
    time.sleep(page_load_wait_seconds)
    print(f'ScrollHeight after scrolling: {browser.execute_script("return document.documentElement.scrollHeight")}')
  return

def links_collection(main_page_link, num_links, start_at_link_num, scroll_limit, page_load_wait_seconds, element_load_wait_seconds):
  print('Working in background...')

  n = 0
  s = 0
  link_num = start_at_link_num
  links_dict = {}

  chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  with chrome_driver as browser:
    browser.get(main_page_link)
    while n < num_links:
      try:
        link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[' + str(
            link_num) + ']/a/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/span/span/object/a'
        page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))
        event_url_long = page.get_attribute('href')
        event_url_cutoff = event_url_long[event_url_long.find('events/') + 7:].find('/')
        event_url = event_url_long[:event_url_long.find('events/') + 7 + event_url_cutoff + 1]
        event_title = page.text
        print(f'Fetching link for event: {event_title}')
        links_dict[event_title + str(n)] = event_url
        link_num += 1
        n += 1
      except Exception as e:
        # print(f'links_collection exception:\n{e}')
        if s < scroll_limit:
          s += 1
          scroll_to_page_end_n_times(browser, s, page_load_wait_seconds)
        else:
          break
  print(f'\nNumber of links: {str(len(links_dict.items()))}')
  return links_dict

def get_location(browser, element_load_wait_seconds):
  try:
    link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[3]'
    page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))
    e_location = page.text
  except Exception as e:
    e_location = 'n/a'
    #print(f'get_location exception:\n{e}')
  return e_location

def get_datetime(browser, element_load_wait_seconds):
  try:
    link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/span'
    page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))
    e_datetime_str = page.text

  except Exception as e:
    e_datetime_str = 'n/a'
    # print(f'get_datetime exception:\n{e}')

  return e_datetime_str

def get_host_and_num_people_responded(browser, element_load_wait_seconds):
  try:
    link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div'
    page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))

    children = page.find_elements(By.XPATH, './child::*')
    e_host = ''
    e_num_people_responded = ''
    for child in children:
      textContent = child.text
      if 'Event by' in textContent:
        e_host = textContent[textContent.find('Event by') + 9:]
      elif 'people responded' in textContent:
        e_num_people_responded = textContent[:textContent.find('people responded')].strip()
      elif 'person responded' in textContent:
        e_num_people_responded = textContent[:textContent.find('person responded')].strip()
      else:
        pass

    if e_host == '':
      e_host = 'n/a'
    if e_num_people_responded == '':
      e_num_people_responded = 'n/a'

  except Exception as e:
    e_host = 'n/a'
    e_num_people_responded = 'n/a'
    # print(f'get_host_and_num_people_responded exception:\n{e}')
  return e_host, e_num_people_responded

def get_description(browser, element_load_wait_seconds):
  try:
    link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[last()]/div/span'
    page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))

    children = page.find_elements(By.XPATH, './child::*')
    for child in children:
      try:
        see_more_btn = child.find_element(By.XPATH, "./div[@role='button']")
        see_more_btn.click()
      except:
        pass

    children = page.find_elements(By.XPATH, './child::*')
    e_description = ''
    for child in children:
      e_description += child.text
      e_description += '\n'

    if 'See less' in e_description:
      e_description = e_description[:e_description.find(' See less')]
    elif 'See more' in e_description:
      e_description = e_description[:e_description.find('... See more')]
    else:
      pass

    if e_description == '':
      e_description = 'n/a'

  except Exception as e:
    e_description = 'n/a'
    # print(f'get_description exception:\n{e}')
  return e_description

def get_image_url(browser, element_load_wait_seconds):
  try:
    link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/a/div/div/div/div/div/img'
    page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))
    img_path = page.get_attribute('src')
  except Exception as ignore:
    try:
      link_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/a/div/div/div/div/img'
      page = WebDriverWait(browser, element_load_wait_seconds).until(EC.visibility_of_element_located((By.XPATH, link_path)))
      img_path = page.get_attribute('src')
    except Exception as e:
      img_path = 'n/a'
      # print(f'get_image_url exception:\n{e}')
  return img_path

def crawl_links(element_load_wait_seconds, current_link):
  e_location = 'n/a'
  e_datetime = 'n/a'
  e_host = 'n/a'
  e_num_people_responded = 'n/a'
  e_description = 'n/a'
  img_path= 'n/a'
  try:
    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    with chrome_driver as browser:
      print(f'Crawling on: {current_link}')

      # Using Selenium
      browser.get(current_link)

      e_location = get_location(browser, element_load_wait_seconds)
      e_datetime = get_datetime(browser, element_load_wait_seconds)
      e_host, e_num_people_responded = get_host_and_num_people_responded(browser, element_load_wait_seconds)
      e_description = get_description(browser, element_load_wait_seconds)
      img_path = get_image_url(browser, element_load_wait_seconds)

  except Exception as e:
    print(f'crawl_links exception:\n{e}')  # if the links are not found in a page, print exception

  return e_location, e_host, e_num_people_responded, e_datetime, e_description, img_path

def main(dict):
  num_links = dict['num_links']
  start_at_link_num = dict['start_at_link_num']
  scroll_limit = dict['scroll_limit']
  page_load_wait_seconds = dict['page_load_wait_seconds']
  element_load_wait_seconds = dict['element_load_wait_seconds']
  event_search_keyword = dict['event_search_keyword']
  main_page_link = f'https://www.facebook.com/events/search/?q={event_search_keyword}'
  pool_size = dict['pool_size']

  links_dict = links_collection(main_page_link, num_links, start_at_link_num, scroll_limit, page_load_wait_seconds, element_load_wait_seconds)

  print('\nInitiating scraping...')
  #pool = Pool(processes=pool_size)  # creates pool of n processes at a time
  #func = partial(crawl_links, element_load_wait_seconds)
  #e_details_list = pool.map(func, list(links_dict.values()))  # maps the function crawl_links (with arg element_load_wait_seconds) with the links_dict.items() input
  e_details_list = [crawl_links(element_load_wait_seconds, link) for link in list(links_dict.values())]

  return_dict = { 'payload' : [] }
  e_details_labels = ['location', 'host', 'numPeopleResponded', 'datetime', 'details', 'imgPath']
  for (e_name, e_link), e_details in zip(links_dict.items(), e_details_list):
    event_dict = {}
    event_dict['link'] = e_link
    event_dict['name'] = e_name[:-1]
    for e_detail_item_label, e_detail_item  in zip(e_details_labels, e_details):
        event_dict[e_detail_item_label] = e_detail_item
    return_dict['payload'].append(event_dict)

    return return_dict