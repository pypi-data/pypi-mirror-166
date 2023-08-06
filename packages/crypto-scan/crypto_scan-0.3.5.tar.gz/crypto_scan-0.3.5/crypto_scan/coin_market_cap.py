import requests
import pandas as pd
from crypto_scan import utils


class CoinMarketCap:

    def __init__(self, api_key):
        self.url = "https://pro-api.coinmarketcap.com"
        # default parameters
        self.headers = {
            "X-CMC_PRO_API_KEY": api_key
        }
        self.default_parameters = {}

    def get_params(self, **kwargs):
        return {**self.default_parameters, **kwargs}

    def request_to_df(self, path, params={}):

        def _print_error(resp, e):
            print(f"ValueError: {e}")
            print(f"Resp: {resp}")
            print(f"Resp content: {resp.content}")
            print(f"Resp json: {resp.json()}")
            print("---" * 10)

        resp = requests.get(f"{self.url}{path}", params=self.get_params(**params), headers=self.headers)
        try:
            data = resp.json()['data']
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame(list(data.values()))
        except Exception as e:
            _print_error(resp, e)
            raise Exception(e)
        return df

    def get_tokens_latest(self, marketcap=0, start=1):
        path = "/v1/cryptocurrency/listings/latest"
        coin_data_df = self.request_to_df(path, params={
            "limit": 5000,
            "market_cap_min": marketcap,
            "start": start,
            "convert": "USD"  # token_list_df
        })
        return utils.json_col_to_df(utils.json_col_to_df(coin_data_df, 'quote'), 'quote_USD')

    def get_all_tokens_latest(self, marketcap=0):
        token_list = []
        start = 1
        while True:
            df = self.get_tokens_latest(marketcap=marketcap, start=start)
            token_list.append(df)
            if len(df) < 5000:
                break
            start += 5000
        return pd.concat(token_list, axis=0).drop_duplicates(['slug'])

    def get_token_info(self, slugs=[]):
        path = "/v2/cryptocurrency/info"
        coin_data_df = self.request_to_df(path, params={
            "slug": ",".join(slugs)
        })
        return coin_data_df

    def get_latest_prices(self, slugs):
        path = "/v1/cryptocurrency/quotes/latest"
        coin_price_df = self.request_to_df(path, params={
            "slug": ','.join(slugs),
        })
        return coin_price_df
