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

    def get_mnemonic(self, mnemonic: str = None) -> MnemonicKey:
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
        print(f"Get some funds here {url}")

    def get_balance(self):
        return self.client.bank.balance(self.mnemonic_key.acc_address)

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
        elif self.chain == "columbus":
            url = "https://fcd.terra.dev/v1/txs/gas_prices"
        r = requests.request(method="GET", url=url)
        return Coins({k: v for k, v in r.json().items() if k == denom})

    def convert_coin(self, coin: Coin, decimals: int = 6) -> dict:
        res = json.loads(coin.to_json())
        res["amount"] = float(int(res["amount"]) / 10**decimals)
        return res

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
        return str(int(amount * exponent)) + denom

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
        return self.client.market.swap_rate(coin, denom)

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

    def swap(
        self,
        coin: str,
        denom: str,
        memo: str = "",
        gas_denom: str = "uusd",
        gas_adj: float = 1.3,
    ) -> dict:
        message = MsgSwap(self.mnemonic_key.acc_address, coin, denom)
        wallet = self.get_wallet(mnemonic=self.mnemonic_key)
        gas = self.get_gas(denom=gas_denom)
        tx = wallet.create_and_sign_tx(
            msgs=[message],
            memo=memo,
            gas_prices=gas,
            gas_adjustment=gas_adj,
            fee_denoms=[gas_denom],
        )
        coin_convert = self.convert_coin(coin=Coin.from_str(coin))
        gas_convert = gas.to_data()[0]
        market_rate = self.get_market_rate(coin, denom)
        market_rate = self.convert_coin(market_rate)
        # Needs fix to account for denom
        print(
            f"Swap {float(coin_convert['amount']) + float(gas_convert['amount']):.2f} {coin_convert['denom']} for {denom} at {market_rate['amount']} {market_rate['denom']}"
        )
        # Temporary (testing)
        s = input("Do you want to proceed with the transaction? (y/n): ")
        return self.client.tx.broadcast(tx) if s.lower() == "y" else None
