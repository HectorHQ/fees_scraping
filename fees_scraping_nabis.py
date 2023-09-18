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
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager



pd.options.display.float_format = "{:,.2f}".format

st.set_page_config('Web Scrapping Fees',':eyes:',layout='wide')

st.title(':eyes: Fees Web :red[Scraping]')

st.text('Please upload the file with the list of Invoices.')


@st.cache()
def generate_driver():
    login_url = "https://app.getnabis.com/sign-in"
    #options = webdriver.ChromeOptions()
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
    #options.add_experimental_option('detach',True)
    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service,options=options)
    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    firefoxOptions.add_argument("--incognito")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    ) 

    
    driver.get(login_url)
    return driver



def get_invoice_fees(invoices):
    driver = generate_driver()
    delay=90
    

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,'//div[@class="css-4uyftl"]')))
        print("La página terminó de cargar")
    except TimeoutException:
        print("La página tardó demasiado en cargar")

    search_url = 'https://app.getnabis.com/nabione-inc-deliveries/app/admin-accounting?page=1&search={}'
    data_list = []
    invoices_skip = []

    for invoice in invoices:
        try:
            driver.get(search_url.format(invoice))
            time.sleep(2)
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="sc-kfPuZi YdThN"]')))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//button[@class="ui compact fluid positive button openAccountingModalButton"]')))
            driver.find_element(By.XPATH, '//button[@class="ui compact fluid positive button openAccountingModalButton"]').click()
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,'//div[@class="sc-crHmcD sc-bkkeKt vVsiZ hnSVCB"]')))
            nabis_fees = driver.find_element(By.XPATH,'//input[@name="totalFees"]').get_attribute('value')
            dict_data = {invoice:nabis_fees}
            data_list.append(dict_data)    
            driver.find_element(By.XPATH,'//button[@class="ui button accountingModalCloseBtn"]').click()
            print(invoice)
        except:
            invoices_skip.append(invoice)
            print(f'Invoices fail => {invoice}')
            continue
        
        

    driver.close()    

    return data_list,invoices_skip    
        





@st.cache()
def load_excel(file_path):
    book = load_workbook(file_path, data_only=True)
    writer = pd.ExcelWriter("temp.xlsx", engine="openpyxl")
    writer.book = book
    writer.save()
    writer.close()
    df = pd.read_excel("temp.xlsx")
    return df


col1,col2 = st.columns([2,1])
with col1:
    list_orders = st.file_uploader('Upload List of invoices file.',accept_multiple_files=False)

if list_orders is not None:
        df = load_excel(list_orders)
        df['Invoice'] = df['Order'].astype('str')
        data_list, invoices_skip = get_invoice_fees(df['Invoice'])
        count_invoices = data_list.shape
        st.write(f'{count_invoices[0]} Invoices to Update')
        
        # Initialize empty lists for 'Invoice' and 'Fees'
        invoices = []
        fees = []

        # Extract data from dictionaries
        for item in data_list:
            for key, value in item.items():
                invoices.append(key)
                fees.append(float(value))

        # Create a DataFrame
        df_download = pd.DataFrame({'Invoice': invoices, 'Fees': fees})


        
        csv = df_download.to_csv().encode('utf-8')

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name= 'data_fees_platform.csv',
            mime='text/csv',
            )
        
        st.dataframe(df_download)
