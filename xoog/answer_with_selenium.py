import requests
from datetime import date, datetime, timedelta
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def download_from_pse():
    start_date = datetime.now() - timedelta(days=30)
    start_date = start_date.strftime("%Y-%m-%d")

    end_date = datetime.now().strftime("%Y-%m-%d")

    # Create Selenium driver
    url = "https://www.pse.pl/dane-systemowe/plany-pracy-kse/biezacy-plan-koordynacyjny-dobowy-bpkd/wielkosci-podstawowe"
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(2)

    # Select 'Export za okres'
    header = driver.find_elements(By.CSS_SELECTOR, "div#_VisioToolbarPortlet_WAR_visioneoportlet_vuiToolbarControlsNavbarCollapse")
    c = header[-1].find_element(By.CSS_SELECTOR, "li#_VisioToolbarPortlet_WAR_visioneoportlet_periodic-export")
    c.click()

    time.sleep(2)

    # Fill input fields with correct dates
    start_field = driver.find_element(By.NAME, "Data od")
    start_field.send_keys(start_date)

    end_field = driver.find_element(By.NAME, "Data do")
    end_field.send_keys(end_date)

    time.sleep(2)

    # Close widget window
    date_widget = driver.find_element(By.CSS_SELECTOR, "div.ui-datepicker-buttonpane.ui-widget-content")
    close_window = date_widget.find_element(By.CSS_SELECTOR, "button.ui-datepicker-close.ui-state-default.ui-priority-primary.ui-corner-all")
    close_window.click()

    # Click on 'Eksport do CSV'
    c = driver.find_element(By.CSS_SELECTOR, "div#_VisioToolbarPortlet_WAR_visioneoportlet_periodic-export-available")
    c = c.find_elements(By.CSS_SELECTOR, "div")
    c = c[3].find_element(By.CSS_SELECTOR, "li#_VisioToolbarPortlet_WAR_visioneoportlet_exportPeriodPDF")
    c.click()

    # Wait for data to download
    time.sleep(500)

    # create name of downloaded file
    start_date = datetime.now() - timedelta(days=30)
    start_date_formatted = start_date.strftime("%Y%m%d")

    end_date = datetime.now().strftime("%Y%m%d")

    name = "PL_BPKD_" + start_date_formatted + "_" + end_date + "_" + datetime.now().strftime("%Y%m%d%H%M%S")

    try:
        df = pd.read_csv("C:/Users/matip/Downloads/" + name + ".csv", encoding="Windows-1250", delimiter=";")
        df['key'] = df['Data'].astype(str) + "-" + df['Godzina'].astype(str)
        return df

    except Exception as e:
        print("An unexpected error occurred ", e)


def download_from_jao():
    header = {
        "AUTH_API_KEY": "" #place for a token
    }

    params = {
        "corridor": "PL-UA",
        "todate": date.today(),
        "horizon": "Daily",
    }

    endpoint = "https://api.jao.eu/OWSMP/getauctions"

    response = requests.get(endpoint, params=params, headers=header)

    if response.status_code == 200:

        result = response.json()

        table = []
        for el in result:
            day_date = '20' + el['identification'][19:21] + "-" + el['identification'][21:23] + "-" + el[
                                                                                                          'identification'][
                                                                                                      23:25]

            for sub in el['results']:
                sub['date'] = day_date
                sub['Hour'] = sub['productHour'][6:8].lstrip("0")
                table.append(sub)

        df = pd.DataFrame(table)

        df['key'] = df['date'].astype(str) + '-' + df['Hour'].astype(str)
        return df
    else:
        print("An unexpected error occurred ")


def main():
    merged_df = pd.merge(download_from_pse(), download_from_jao(), on='key', how='inner')
    print(merged_df)


if __name__ == "__main__":
    main()