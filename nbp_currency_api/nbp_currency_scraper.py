import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, Union


def download_curr_data(selected_curr):
    this_moment = datetime.now()

    days = [("/" + (this_moment - relativedelta(years=i+1, days=-1)).strftime("%Y-%m-%d") +
             "/" + (this_moment - relativedelta(years=i)).strftime("%Y-%m-%d") + "/") for i in range(0, 6)]
    days.reverse()

    params = {
        "format": "json",
    }

    effectiveDate = []
    mid = []

    for day in days:
        endpoint = "https://api.nbp.pl/api/exchangerates/rates/a/" + selected_curr + day
        response = requests.get(url=endpoint, params=params)

        if response.status_code != 200:

            return {'success': False, 'status_code': response.status_code}

        ex_dict = response.json()["rates"]

        for curr_day in ex_dict:
            effectiveDate.append(curr_day['effectiveDate'])
            mid.append(curr_day['mid'])

    ready_dict = {
            'date': effectiveDate,
            selected_curr: mid,
           }

    return {'success': True, 'data': pd.DataFrame(ready_dict)}


def download_gold_data():
    this_moment = datetime.now()

    days = [("/" + (this_moment - relativedelta(years=i+1, days=-1)).strftime("%Y-%m-%d") +
             "/" + (this_moment - relativedelta(years=i)).strftime("%Y-%m-%d") + "/") for i in range(0, 6)]
    days.reverse()

    params = {
        "format": "json",
    }

    effectiveDate = []
    mid = []

    for day in days:
        endpoint = "http://api.nbp.pl/api/cenyzlota" + day
        response = requests.get(url=endpoint, params=params)

        ex_dict = response.json()

        for current_day in ex_dict:
            effectiveDate.append(current_day['data'])
            mid.append(current_day['cena'])

    ready_dict = {
            'date': effectiveDate,
            'gold_price': mid,
           }

    return pd.DataFrame(ready_dict)


def make_main_table(selected_curr: list) -> Dict[str, Union[bool, pd.DataFrame]]:
    a_dic = (download_curr_data(selected_curr[0]))
    b_dic = (download_curr_data(selected_curr[1]))
    c_dic = (download_curr_data(selected_curr[2]))

    if not (a_dic['success'] and b_dic['success'] and c_dic['success']):
        print("Błędny symbol waluty")
        return {'success': False}

    a = a_dic['data']
    b = b_dic['data']
    c = c_dic['data']

    merged_df = pd.merge(a, b, on='date', how='left')
    merged_df = pd.merge(merged_df, c, on='date', how='left')

    merged_df['date'] = pd.to_datetime(merged_df['date'])

    gold_df = download_gold_data()
    gold_df['date'] = pd.to_datetime(gold_df['date'])

    data = {'date': pd.date_range(start=min(merged_df["date"]), end=max(merged_df["date"]), freq='D')}
    full_df = pd.DataFrame(data)

    curr_df = pd.merge(full_df, merged_df, on='date', how='left')
    curr_df = curr_df.interpolate(method='linear')

    gold_df = pd.merge(full_df, gold_df, on='date', how='left')

    # uzupełnienie brakujących danych
    gold_df = gold_df.interpolate(method='linear')

    curr_df['gold_price_' + selected_curr[0]] = round(gold_df['gold_price'] / curr_df[selected_curr[0]], 2)
    curr_df['gold_price_' + selected_curr[1]] = round(gold_df['gold_price'] / curr_df[selected_curr[1]], 2)
    curr_df['gold_price_' + selected_curr[2]] = round(gold_df['gold_price'] / curr_df[selected_curr[2]], 2)

    return {'success': True, 'data': curr_df[['date'] + ['gold_price_' + curr_t for curr_t in selected_curr]]}


def draw_plot(full_df, selected_curr):
    plt.xticks(rotation=45, fontsize=10)

    plt.plot(full_df['date'], full_df['gold_price_' + selected_curr[0]], label=selected_curr[0].upper())
    plt.plot(full_df['date'], full_df['gold_price_' + selected_curr[1]], label=selected_curr[1].upper())
    plt.plot(full_df['date'], full_df['gold_price_' + selected_curr[2]], label=selected_curr[2].upper())

    plt.legend(loc='upper left')

    plt.title('Gold Prices in Different Currencies')
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Gold Price', fontsize=10)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    # curr = ["usd", "chf", "gbp"]

    curr = []
    for i in range(3):
        curr.append(input(f"Podaj symbol {i + 1} waluty: ").lower())

    df_dic = make_main_table(curr)

    if df_dic['success']:
        ready_df = df_dic['data']

        draw_plot(ready_df, curr)






