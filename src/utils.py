from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.localterra import LocalTerra
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.coins import Coins, Coin
from terra_sdk.core.market import MsgSwap
from terra_sdk.core.bank import MsgSend
import requests
import json


class Utils:
    def __init__(self, chain: str = "bombay"):
        self.chain = chain.lower()
        self.client = self.get_client(chain=chain)

    def get_client(self, chain: str = "bombay") -> LCDClient:
        """
        Get LCD client for a given chain
        args:
            chain: str -- bombay
        returns:
            LCDClient
        """
        if self.chain == "bombay":
            terra = LCDClient("https://bombay-lcd.terra.dev", "bombay-12")
        elif self.chain == "local":
            terra = LocalTerra()
        elif self.chain == "columbus":
            terra = LCDClient("https://lcd.terra.dev", "columbus-5")
        else:
            raise Exception("Invalid chain, must be local, bombay, local or columbus")
        return terra

    def create_mnemonic(self) -> MnemonicKey:
        """
        Create a wallet
        returns:
            MnemonicKey
        """
        self.mnemonic = MnemonicKey()
        return self.mnemonic

    def get_mnemonic(self, mnemonic: str) -> MnemonicKey:
        """
        Get mnemonic key from a given mnemonic
        args:
            mnemonic: str -- "blue cone cool breeze ... cool bannanas"
        returns:
            MnemonicKey
        """
        self.mnemonic_key = MnemonicKey(mnemonic=mnemonic)
        return self.mnemonic_key

    def get_wallet(self, mnemonic: MnemonicKey) -> LCDClient.wallet:
        """
        Get wallet address from a given client and mnemonic
        args:
            client: LCDClient -- self.client
            mnemonic: MnemonicKey -- mnemonic
        returns:
            self.client.wallet
        """
        return self.client.wallet(mnemonic)

    def get_funds(self, url="https://faucet.terra.money/"):
        print("Get some funds here {}".format(url))

    def get_balance(self):
        balance = self.client.bank.balance(self.mnemonic_key.acc_address)
        return balance

    def get_gas(self, denom: str = "uusd") -> Coins:
        """
        Get gas for a given chain and denom (CW20 main coin)
        args:
            denom: str -- uusd
        returns:
            Coins
        """

        if self.chain == "bombay":
            url = "https://bombay-fcd.terra.dev/v1/txs/gas_prices"
        if self.chain == "columbus":
            url = "https://fcd.terra.dev/v1/txs/gas_prices"
        r = requests.request(method="GET", url=url)
        gas = Coins({k: v for k, v in r.json().items() if k == denom})
        return gas

    def convert_denom(
        self, amount: float, denom: str = "uusd", decimals: int = 6
    ) -> str:
        """
        Converts a given amount of a given denom to a string.
        This string can be then used to creat a Coins object
        args:
            amount: float -- 100
            denom: str -- uusd
            decimals: int -- 6
        returns:
            str -- 100000000uusd
        """
        exponent = 10**decimals
        result = str(int(amount * exponent)) + denom
        return result

    def get_market_rate(
        self, coin: str = "100000000uusd", denom: str = "uluna"
    ) -> Coin:
        """
        Get market rate for a given coin and denom
        args:
            coin: str -- 100000000uusd
            denom: str -- uluna
        returns:
            Coin
        """
        result = self.client.market.get_price(coin1, denom)

    def get_luna_price(self, denom: str = "uusd", interval="5m") -> dict:
        """
        Get luna price for a given denom and interval
        args:
            denom: str -- uusd
            interval: str -- 5m
        returns:
            dict
        """

        url = f"https://fcd.terra.dev/v1/market/price?denom={denom}&interval={interval}"
        req = requests.request(method="GET", url=url)
        return req.json()
