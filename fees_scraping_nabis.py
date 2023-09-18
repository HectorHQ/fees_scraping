import streamlit as st
from seleniumbase import webdriver
from seleniumbase.webdriver.common.by import By
from seleniumbase.webdriver import Keys, ActionChains
from seleniumbase.webdriver.support.wait import WebDriverWait
from seleniumbase.common import NoSuchElementException, ElementNotInteractableException
from seleniumbase.webdriver.support import expected_conditions as EC
from seleniumbase.common.exceptions import TimeoutException
import pandas as pd
import time
from seleniumbase.webdriver.chrome.options import Options
from seleniumbase.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook



pd.options.display.float_format = "{:,.2f}".format

st.set_page_config('Web Scrapping Fees',':eyes:',layout='wide')

st.title(':eyes: Fees Web :red[Scraping]')

st.text('Please upload the file with the list of Invoices.')


with st.echo():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    @st.cache_resource()
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    driver = get_driver()
    driver.get("http://example.com")

    st.code(driver.page_source)






# @st.cache()
# def generate_driver():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     login_url = "https://app.getnabis.com/sign-in"
#     driver.get(login_url)
    
#     return driver

# options = Options()
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')
# options.add_argument('--incognito')
# options.add_experimental_option('detach',True)


# st.cache()
# def get_invoice_fees(invoices, driver):
#     driver = driver
#     delay=90
    


#     try:
#         WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,'//div[@class="css-4uyftl"]')))
#         print("La página terminó de cargar")
#     except TimeoutException:
#         print("La página tardó demasiado en cargar")

#     search_url = 'https://app.getnabis.com/nabione-inc-deliveries/app/admin-accounting?page=1&search={}'
#     data_list = []
#     invoices_skip = []

#     for invoice in invoices:
#         try:
#             driver.get(search_url.format(invoice))
#             time.sleep(2)
#             WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="sc-kfPuZi YdThN"]')))
#             WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//button[@class="ui compact fluid positive button openAccountingModalButton"]')))
#             driver.find_element(By.XPATH, '//button[@class="ui compact fluid positive button openAccountingModalButton"]').click()
#             WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,'//div[@class="sc-crHmcD sc-bkkeKt vVsiZ hnSVCB"]')))
#             nabis_fees = driver.find_element(By.XPATH,'//input[@name="totalFees"]').get_attribute('value')
#             dict_data = {invoice:nabis_fees}
#             data_list.append(dict_data)    
#             driver.find_element(By.XPATH,'//button[@class="ui button accountingModalCloseBtn"]').click()
#             print(invoice)
#         except:
#             invoices_skip.append(invoice)
#             print(f'Invoices fail => {invoice}')
#             continue
        
        

#     driver.close()    

#     return data_list,invoices_skip    
        

# st.cache()
# def load_excel(file_path):
#     book = load_workbook(file_path, data_only=True)
#     writer = pd.ExcelWriter("temp.xlsx", engine="openpyxl")
#     writer.book = book
#     writer.save()
#     writer.close()
#     df = pd.read_excel("temp.xlsx")
#     return df


# col1,col2 = st.columns([2,1])
# with col1:
#     list_orders = st.file_uploader('Upload List of invoices file.',accept_multiple_files=False)

# if list_orders is not None:
#         df = load_excel(list_orders)
#         df['Invoice'] = df['Order'].astype('str')
#         driver = generate_driver()
#         data_list, invoices_skip = get_invoice_fees(df['Invoice'],driver=driver)
#         count_invoices = data_list.shape
#         st.write(f'{count_invoices[0]} Invoices to Update')
        
#         # Initialize empty lists for 'Invoice' and 'Fees'
#         invoices = []
#         fees = []

#         # Extract data from dictionaries
#         for item in data_list:
#             for key, value in item.items():
#                 invoices.append(key)
#                 fees.append(float(value))

#         # Create a DataFrame
#         df = pd.DataFrame({'Invoice': invoices, 'Fees': fees})


        
#         csv = df.to_csv().encode('utf-8')

#         st.download_button(
#             label="Download data as CSV",
#             data=csv,
#             file_name= 'data_fees_platform.csv',
#             mime='text/csv',
#             )
        
#         st.dataframe(df)
