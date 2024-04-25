import requests
import json
import pandas as pd

currencies = ['USD', 'CHF', 'EUR' , 'GBP', 'JPY']
how_many_last = 25

responses = []

for curr in currencies:
    url = f'http://api.nbp.pl/api/exchangerates/rates/a/{curr}/last/{how_many_last}?format=json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        responses.append(data)

        with open(f'{curr}_data.json', 'w') as file:
            json.dump(data, file, indent=4)
        print(f'Dane dla waluty {curr} zostały zapisane do pliku {curr}_data.json')
    else:
        print(f'Nie udało się pobrać danych dla waluty {curr}. Kod statusu:', response.status_code)

df = pd.DataFrame(responses[0])
df

currencies_info = []
currency_rates_details = []

for response in responses:
  for rate in response["rates"]:
    rate["code"] = response["code"]

  currency_rates_details.append(response["rates"])
  response.pop("table", None)
  response.pop("rates", None)
  currencies_info.append(response)

currency_rates_details = sum(currency_rates_details, [])

df_currencies_info = pd.DataFrame(currencies_info)
df_currency_rates_details = pd.DataFrame(currency_rates_details)
df_currency_rates_details

df_currencies_info.to_json("currencies_info.json", orient="records", indent=4)
df_currency_rates_details.to_json("currency_rates_details.json", orient="records", indent=4)
print('Data has been normalized and saved')