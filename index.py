from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

pricefilter = 829
driver = webdriver.Chrome()
url = "https://www.turismocity.com.ar/vuelos-baratos-a-LAX-Los_Angeles_Intl?from=BUE&d=20250901.20250930&currency=USD"

while True:
    driver.get(url)
    time.sleep(1) 

    flights = []
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.tr-body")
    for row in rows:
        try:
            date_departure = row.find_element(By.CSS_SELECTOR, "td:nth-child(1) div").text
            date_return = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) div").text
            airline = row.find_element(By.CSS_SELECTOR, "td:nth-child(6) img").get_attribute("alt") or "null"
            price = row.find_element(By.CSS_SELECTOR, "td:nth-child(7) span").text
            link = row.find_element(By.CSS_SELECTOR, "td:nth-child(8) a").get_attribute("href")
        
            price_numeric = int(''.join([char for char in price if char.isdigit()]))
            
            flight_data = [date_departure, date_return, airline, price_numeric, link]
            flights.append(flight_data)
        
            print("Date departure: " + date_departure, " - Date return: " + date_return, " - Airline: " + airline, " - Price: USD $" + str(price_numeric))
            
            if price_numeric < pricefilter:
                df = pd.DataFrame(flights, columns=["Fecha de Salida", "Fecha de Regreso", "Aerolínea", "Precio", "Enlace"])
                df.to_excel("vuelos.xlsx", index=False)
        except Exception as e:
            print(f"Error al procesar fila: {e}")
            print(f"Detalles del error: {e}")
