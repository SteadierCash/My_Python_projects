import requests
from datetime import date, datetime, timedelta
import pandas as pd


def download_from_pse():
    try:
        df = pd.read_csv("PL_BPKD_20240330_20240429_20240429163947.csv", encoding="Windows-1250", delimiter=";")
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

    response = requests.get(endpoint, params=params ,headers=header)

    if response.status_code == 200:

        result = response.json()
        
        table = []
        for el in result:
            day_date = '20' + el['identification'][19:21] + "-"  + el['identification'][21:23] + "-" + el['identification'][23:25]

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

