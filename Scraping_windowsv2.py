import sys
sys.path.insert(0,'C:\Tools\chromedriver')

import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import chromedriver_autoinstaller
import re
import json
from datetime import datetime
import time
import random


hora_inicio = datetime.now()
# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')

# Setup Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless') # ensure GUI is off
#firefox_options.add_argument('--no-sandbox')
#firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')

# # set path to chromedriver as per your configuration
chromedriver_autoinstaller.install()

def scrapebyPages(min, max):
  #Range of pages from the total search to scrape in.
  #It is recomended to cover a range of one hundred pages in each iteration of this section.
  data = pd.DataFrame()
  for i in range(min,max):

      print(f'************************************')
      print(f'WEB SCRAPING FROM SEARCH PAGE #{i}')
      pag = i

      # ------- DATA TU CARRO ------------
      #url = f'https://vehiculos.tucarro.com.co/renault-duster_Desde_{49*i}_NoIndex_True' #Renault duster - Jackson
      #url = f'https://vehiculos.tucarro.com.co/corolla_Desde_{49*i}_NoIndex_True' #Toyota Corolla - Laura
      url = f'https://vehiculos.tucarro.com.co/chevrolet-onix_Desde_{49*i}_MODEL_123123_NoIndex_True' #Chevrolet Onix - Jackson
      #url = f'https://vehiculos.tucarro.com.co/susuki-swift_Desde_{49*i}_NoIndex_True'  #Susuki Swift - Laura
      #url = f'https://vehiculos.tucarro.com.co/mazda-2_Desde_{49*i}_MODEL_59481_NoIndex_True' #Mazda 2 - Jackson

      #--------- MERCADOLIBRE
      #url = f'https://carros.mercadolibre.com.co/renault-duster_Desde_{49*i}_NoIndex_True' #Renault duster - Jackson
      # url = f'https://carros.mercadolibre.com.co/corolla_Desde_{49*i}_NoIndex_True' #Toyota Corolla - Laura
      # url = f'https://carros.mercadolibre.com.co/chevrolet-onix_Desde_49_MODEL_123123_NoIndex_True' #Chevrolet Onix - Jackson
      # url = f'https://carros.mercadolibre.com.co/susuki-swift_Desde_{49*i}_NoIndex_True'  #Susuki Swift - Laura
      # url = f'https://carros.mercadolibre.com.co/mazda-2_Desde_{49*i}_MODEL_59481_NoIndex_True' #Mazda 2 - Jackson
      #url = f'https://carros.mercadolibre.com.co/renault_Desde_{49*i}_MODEL_64855_NoIndex_True'

      # print(url)
      #driver = webdriver.Firefox(options=firefox_options)
      driver = webdriver.Chrome(options=chrome_options)
      driver.get(url)
      driver.implicitly_wait(10)
      html = driver.page_source
      soup = bs(html,'lxml')

      #Get href
      links = gethref(soup)

      #Scrapping
      # for i in range(0,5):
      #   soup = scrapper(links[i])
      #   # print(soup)

      p = []
      # cols = ['car_model','price','year_model','kms']
      # data = pd.DataFrame(columns=cols)
      #Scrapping a los inmuebles filtrados
      # for i in range(len(links)):
      for i in range(0,len(links)):
          print('Scrapping', i+1, '/', len(links), '...')
          p.append(scrapper(links[i]))
          print(f'Este es el valor de p[i]: {p[i]}')

      # #append list to DataFrame
      #data = data.append(p, ignore_index=True)
      data = pd.concat([data, pd.DataFrame(p)], ignore_index = True)
      # print(f'This is the dataset:\n {data}')

  #Close the web browser tab
  driver.close()

  # quit the driver
  driver.quit()

  return data

#Function to get 'href' from each article item
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
    #driver = webdriver.Firefox(options=firefox_options)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(random.randint(1,20))
    # Scrape
    driver.implicitly_wait(60)
    driver.get(url_car)
    driver.refresh()
    driver.implicitly_wait(30)
    html=driver.page_source
    #url_carro = url_car
    #Linea para depurar los enlaces
    #print("URL CARRO:", url_car)
    #Obtaining the html from the web page after applying Selenium
    soup = bs(html,'lxml')

    #Create a list to store info obtained from one particular property
    features = []

    #Applying function to obtain variables defined from one particular property
    features = extract_cars_features(soup,url_car)

    #Close the web browser tab
    driver.close()

    # quit the driver
    driver.quit()

    return(features)

def extract_cars_features(soup,url_car):
    #print(soup)
    features_list = []

    # car_name
    try:
        car_name = soup.find('h1',{'class': 'ui-pdp-title'}).text
        car_name = car_name.replace(',', '')
        features_list.append(str(car_name))
    # print(f"Car's name is: {car_name}")
    except:
        car_name = 'N/A'
        features_list.append(str(car_name))

    # price
    try:
        price=soup.find('div',{'class': 'ui-pdp-price__second-line'}).text
        price=price.replace('$','').replace(',','')
        features_list.append(price)
    # print(f"Car's price is: {price}")
    except:
        price = 0
        features_list.append(0.0)

    # year_car
    try:
        year_kms_datePub = soup.find('div',{'class': 'ui-pdp-header__subtitle'}).text.split(' ')
        year = year_kms_datePub[0]
        features_list.append(str(year))
    except:
        year = 0
        features_list.append(str(year))

    # kms
    try:
        year_kms_datePub = soup.find('div',{'class': 'ui-pdp-header__subtitle'}).text.split(' ')
        kms = year_kms_datePub[2]
        kms = kms.replace('.', ',')
        features_list.append(kms)
    except:
        kms = 0
        features_list.append(kms)

    #Data de combustible
    try:
        color_temp = soup.find('div', {'class': 'andes-table__header__container'}, text='Color').find_next('td')
        color = color_temp.text.strip()
        color = color.replace(',','')
        features_list.append(str(color))
    except:
        try:
            script = soup.find("script", {'type': 'application/ld+json'})
            if script:
                # Obtener el contenido del script
                script_content = script.string

                # Utilizar expresiones regulares para extraer el color y el tipo de combustible
                color_match = re.search(r'"color":"([^"]+)"', script_content)
                #fuel_type_match = re.search(r'"fuelType":"([^"]+)"', script_content)

                if color_match:
                    color = color_match.group(1)
                    features_list.append(str(color))
                    # print(f"Color del carro: {color}")
                else:
                    color = 'N/A'
                    features_list.append(str(color))
            else:
                print("No se encontró el script de Color.")
        except:
            pass
        #color = 'N/A'
        #features_list.append(color)
    try:
        fuel_type_temp = soup.find('div', {'class': 'andes-table__header__container'}, text='Tipo de combustible').find_next('td')
        fuel_type = fuel_type_temp.text.strip()
        features_list.append(str(fuel_type))
    except:
        try:
            script = soup.find("script", {'type': 'application/ld+json'})
            if script:
                # Obtener el contenido del script
                script_content = script.string

                # Utilizar expresiones regulares para extraer el color y el tipo de combustible
                #color_match = re.search(r'"color":"([^"]+)"', script_content)
                fuel_type_match = re.search(r'"fuelType":"([^"]+)"', script_content)

                if fuel_type_match:
                    fuel_type = fuel_type_match.group(1)
                    features_list.append(str(fuel_type))
                    # print(f"Tipo de combustible: {fuel_type}")
                else:
                    fuel_type = 0
                    features_list.append(str(fuel_type))

            else:
                print("No se encontró el script de Combustible.")
        except:
            pass
        #fuel_type = 'N/A'
        #features_list.append(fuel_type)

    try:
      ubicacion_div = soup.find('h3', {'class': 'ui-seller-info__status-info__title ui-vip-seller-profile__title'}, text='Ubicación del vehículo')
      if ubicacion_div:
          ubicacion_text = ubicacion_div.find_next('p', {'class': 'ui-seller-info__status-info__subtitle'}).text
          location = ubicacion_text.split(' - ')[-1]
          features_list.append(str(location))
      else:
          location = 'N/A'
          features_list.append(location)
    except Exception as e:
      print(f"Hubo un error al extraer la ubicación: {e}")
      features_list.append('ERROR')
      # kms
    try:
      url_carro = url_car
      features_list.append(str(url_carro))
    except:
      url_carro = 'N/A'
      features_list.append(url_carro)
    # print(f"Kms: {kms}")

    # # date_publication_1
    # datePub = ' '.join(year_kms_datePub[7:])
    # features_list.append(datePub)
    # # print(f"Publication date: {datePub}")

    # print(features_list)

    return features_list



####------------------- linea del main

data = scrapebyPages(1,6)
# scrapebyPages(1,2)


cols=['car_model','price','year_model','kms','colour','fuel_type','location','url_car']
print(data.shape)
data.columns=cols
data.head()

#data.to_csv('usedCarsCol_chOnix_200224_small.csv', encoding='utf-8', index=False)

fecha_actual = datetime.now().strftime("%d%m%Y")
nombre_archivo = f"Tucarro_{fecha_actual}.csv"
data.to_csv(nombre_archivo, index=False)
print("Archivo creado con exito")
print(f'Hora inicio: {hora_inicio}')
hora_final=datetime.now()
print(f'Hora final: {hora_final}')
duracion_temp = hora_final - hora_inicio
duracion = str(duracion_temp).split('.')
print(f"Tuvo una duración de: {duracion[0]}")

def test():
    data = pd.read_csv("Tucarro_05032024.csv")
    print(data.dtypes)
    return test()

#test()