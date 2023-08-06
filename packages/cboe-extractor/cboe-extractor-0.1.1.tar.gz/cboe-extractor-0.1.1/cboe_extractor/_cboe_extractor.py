from urllib import response
import requests
import pandas as pd

class CBOEExtractor:
    def __init__(self, cboe_host: str):
        self.cboe_host = cboe_host
        response = requests.get(
            url="https://{host}/api/global/delayed_quotes/options/_SPX.json".format(
                host=self.cboe_host
            )
        )
        if response.ok:
            self.data = response.json()

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.data["data"]["options"])
        df["last_trade_time"] = pd.to_datetime(df["last_trade_time"])
        return df