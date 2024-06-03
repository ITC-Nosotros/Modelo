import sys
sys.path.insert(0,'/usr/bin/chromedriver')

import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from lxml import etree
import chromedriver_autoinstaller
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# # set path to chromedriver as per your configuration
#chromedriver_autoinstaller.install()

def scrapebyPages(min, max):
    # Range of pages from the total search to scrape in.
    # It is recomended to cover a range of one hundred pages in each iteration of this section.
    data = pd.DataFrame()
    for i in range(min, max):

        print(f'************************************')
        print(f'WEB SCRAPING FROM SEARCH PAGE #{i}')
        pag = i

        #url = f'https://vehiculos.tucarro.com.co/renault-duster_Desde_{49*i}_NoIndex_True'
        #url = f'https://vehiculos.mercadolibre.com.co/swift_Desde_{49 * i}_NoIndex_True'  #Susuki swift
        #url = f'https://vehiculos.tucarro.com.co/maxda-cx-30_Desde_{49*i}_NoIndex_True' #Mazda CX 30
        url = f'https://carros.mercadolibre.com.co/renault/logan/renault-logan_Desde_{49*i}_NoIndex_True' #Renault logan

        # print(url)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source
        soup = bs(html, 'lxml')

        # Get href
        links = gethref(soup)

        # Scrapping
        # for i in range(0,5):
        #   soup = scrapper(links[i])
        #   # print(soup)

        p = []
        # cols = ['car_model','price','year_model','kms']
        # data = pd.DataFrame(columns=cols)
        # Scrapping a los inmuebles filtrados
        # for i in range(len(links)):
        for i in range(0, len(links)):
            print('Scrapping', i + 1, '/', len(links), '...')
            p.append(scrapper(links[i]))
            print(f'Este es el valor de p[i]: {p[i]}')

        # #append list to DataFrame
        # data = data.append(p, ignore_index=True)
        data = pd.concat([data, pd.DataFrame(p)], ignore_index=True)
        # print(f'This is the dataset:\n {data}')

    # Close the web browser tab
    driver.close()

    # quit the driver
    driver.quit()

    return data


# Function to get 'href' from each article item
def gethref(soup):
    links = []
    for link in soup.findAll('a'):
        url_car = link.get('href')
        if 'MCO-' in url_car:
            # print(url_car)          %Print each car url as a validity test
            links.append(url_car)

    print("Href obtained: ", len(links))

    # for article in soup.find_all('article'):
    #     url = article.find('a', href=True)
    #     if url:
    #         link = url['href']
    #         links.append(link)
    # print("Href obtained: ", len(links))

    return links
    # return


def scrapper(url_car):
    # set up the webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Scrape
    driver.get(url_car)
    driver.implicitly_wait(10)
    html = driver.page_source
    # Linea para depurar los enlaces
    # print("URL CARRO:", url_car)
    # Obtaining the html from the web page after applying Selenium
    soup = bs(html, 'lxml')

    # Create a list to store info obtained from one particular property
    features = []

    # Applying function to obtain variables defined from one particular property
    features = extract_cars_features(soup)

    # Close the web browser tab
    driver.close()

    # quit the driver
    driver.quit()

    return (features)


def extract_cars_features(soup):
    features_list = []

    # car_name
    try:
        car_name = soup.find('h1', {'class': 'ui-pdp-title'}).text
        features_list.append(car_name)
        # print(f"Car's name is: {car_name}")
    except:
        car_name = ' '
        features_list.append(car_name)

    # price
    try:
        price = soup.find('div', {'class': 'ui-pdp-price__second-line'}).text
        features_list.append(price)
        # print(f"Car's price is: {price}")
    except:
        price = 0
        features_list.append(price)

    # year_car
    try:
        year_kms_datePub = soup.find('div', {'class': 'ui-pdp-header__subtitle'}).text.split(' ')
        year = year_kms_datePub[0]
        features_list.append(year)
    except:
        year = 0
        features_list.append(year)

    # kms
    try:
        year_kms_datePub = soup.find('div', {'class': 'ui-pdp-header__subtitle'}).text.split(' ')
        kms = year_kms_datePub[2]
        features_list.append(kms)
    except:
        kms = 0
        features_list.append(kms)

    # Data de <script>
    try:
        script = soup.find("script", {'type': 'application/ld+json'})
        if script:
            # Obtener el contenido del script
            script_content = script.string

            # Utilizar expresiones regulares para extraer el color y el tipo de combustible
            color_match = re.search(r'"color":"([^"]+)"', script_content)
            fuel_type_match = re.search(r'"fuelType":"([^"]+)"', script_content)

            # Imprimir los resultados
            if color_match:
                color = color_match.group(1)
                features_list.append(color)
                # print(f"Color del carro: {color}")

            if fuel_type_match:
                fuel_type = fuel_type_match.group(1)
                features_list.append(fuel_type)
                # print(f"Tipo de combustible: {fuel_type}")

        else:
            print("No se encontró el script JavaScript en la página.")
    except:
        color = 0
        features_list.append(color)
        fuel_type = 0
        features_list.append(fuel_type)
    # print(f"Kms: {kms}")

    # # date_publication_1
    # datePub = ' '.join(year_kms_datePub[7:])
    # features_list.append(datePub)
    # # print(f"Publication date: {datePub}")

    # print(features_list)

    return features_list


data = scrapebyPages(1, 10)
# scrapebyPages(1,2)


cols = ['car_model', 'price', 'year_model', 'kms', 'colour', 'fuel_type']
print(data.shape)
data.columns = cols
data.head()

# data.to_csv('usedCarsCol_chOnix_200224_small.csv', encoding='utf-8', index=False)
# Obtener la fecha actual
fecha_actual = datetime.now().strftime("%d%m%Y")
# Construir el nombre del archivo con la fecha
nombre_archivo = f"Tucarro_{fecha_actual}.csv"
# Guardar el DataFrame en un archivo CSV con el nombre que contiene la fecha
data.to_csv(nombre_archivo, index=False)