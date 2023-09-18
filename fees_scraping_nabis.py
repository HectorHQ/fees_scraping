import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
from openpyxl import load_workbook
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

login_url = "https://app.getnabis.com/sign-in"

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_experimental_option('detach',True)

driver = get_driver()
driver.get(login_url)

driver

