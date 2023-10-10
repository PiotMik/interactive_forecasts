import pandas as pd
import requests

if __name__ == '__main__':
    url = "http://localhost:8080/data"
    body = {"dataset": "MarketData_202309_v0",
            "mnemonics": ["USGDPT", "WDGDPT"]}
    response = requests.get(url, params=body)
    data = pd.read_json(response.json(), orient='columns')

    url = "http://localhost:8080/forecast/simple_mapping"
    payload = {"dataset": "MarketData_202309_v0",
               "inputs": {"explanatory_series": "WDGDPT",
                          "explained_series": "USGDPT",
                          "date": "2023-09",
                          "mapping": {"period": "YoY",
                                      "type": "percentage growth"}
                          }
               }
    response = requests.get(url, json=payload)
    response.json()

    url = "http://localhost:8080/forecast/shift_data"
    payload = {"dataset": "MarketData_202309_v0",
               "inputs": {"scalar": 100.0}
               }
    response = requests.get(url, json=payload)
    response.json()

    body = {"dataset": "MarketData_202309_v0",
            "variable": "USGDPT",
            "date": "1980-01",
            "value": 200.0}
    response = requests.put(url, params=body)
    response.json()
