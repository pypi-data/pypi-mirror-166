import requests
import pandas as pd
from crypto_scan.utils import validate_dateformat, transfer_date_format, valid_chain
from crypto_scan.configs import COIN_GECHO_CHAIN_DATA

# https://www.coingecko.com/en/api/documentation


class CoinGecko:

    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        # default parameters
        self.default_parameters = {
        }

    def get_params(self, **kwargs):
        return {**self.default_parameters, **kwargs}

    def request_to_df(self, path, params={}):

        def _print_error(resp, e):
            print(f"ValueError: {e}")
            print(f"Resp: {resp}")
            print(f"Resp content: {resp.content}")
            print(f"Resp json: {resp.json()}")
            print("---" * 10)

        resp = requests.get(f"{self.url}{path}", params=self.get_params(**params))
        try:
            data = resp.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame(list(data.values()))
        except Exception as e:
            _print_error(resp, e)
            raise Exception(e)
        return df

    def get_coins(self):
        path = "/coins/list"
        return self.request_to_df(path)

    def get_coin_markets(self):
        path = "/coins/markets"
        params = {
            "vs_currency": "usd"
        }
        return self.request_to_df(path, params=params)

    def get_chains(self):
        path = "/asset_platforms"
        return self.request_to_df(path)

    def get_coin_history(self, coin_id, date):
        if not validate_dateformat(date, "%Y-%m-%d"):
            raise ValueError(f"Invalid date format {date}, should be %Y-%m-%d")
        api_date_format = transfer_date_format(date, "%Y-%m-%d", "%d-%m-%Y")
        url = f"{self.url}/coins/{coin_id}/history"
        params = {
            "date": api_date_format,
            "localization": False,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()

    def get_coin_by_chain_contract(self, chain, contract_addr):
        valid_chain(chain)
        chain_id = COIN_GECHO_CHAIN_DATA[chain]['chain_id']
        url = f"{self.url}/coins/{chain_id}/contract/{contract_addr}"
        r = requests.get(url)
        return r.json()

    def get_coin_id_by_chain(self, chain):
        valid_chain(chain)
        return COIN_GECHO_CHAIN_DATA[chain]['coin_id']

    def get_coin_market_inusd_by_chain_contract(self, chain, contract_addr, days_back='max'):
        url = f"{self.url}/coins/{chain}/contract/{contract_addr}/market_chart"
        params = {
            "vs_currency": 'usd',
            "days": days_back,
        }
        r = requests.get(url, params=self.get_params(**params))
        return r.json()
