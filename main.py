from flask import Flask,render_template,request
from datetime import datetime
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://www.newsnow.co.uk/h/Industry+Sectors/Energy+&+Utilities/Oil+&+Gas?type=ln'
response = requests.get(url)
print(response.status_code)

newsnow = []
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a', {'class':'hll'})
for ln in links:
    newsnow.append(ln.text + " " + ln['href'])


app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return search_func()
    if request.method == 'POST':
        driver = webdriver.Chrome(executable_path= r"C:\Users\21575\Downloads\chromedriver_win32\chromedriver.exe")
        driver.get('https://www.google.com')
        driver.maximize_window()
        search_query = driver.find_element_by_name('q')
        search_query.click()
        search_query.send_keys('"npdc" petroleum')
        search_query.submit()

        news_tab = driver.find_element_by_link_text('News')
        #https://selenium-python.readthedocs.io/locating-elements.html
        news_tab.click()

        new_list = []
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            print(elem.get_attribute("href"))
            if 'google' not in elem.get_attribute("href"):
                new_list.append(elem.get_attribute("href"))
        driver.quit()

        date_and_time = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')).replace('-','').replace(':','')
        df = pd.Series(newsnow + new_list)
        df.to_excel('press_cuts' + date_and_time + ".xlsx")
        return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
