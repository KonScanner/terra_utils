from src.utils import Utils
import os
import time

if __name__ == "__main__":
    ut = Utils(chain="columbus")
    mnemonic = ut.get_mnemonic(mnemonic=os.getenv("TERRA_MNEMONIC"))
    # print(mnemonic.acc_address, sep="\n")
    coin = ut.convert_denom(1, "uusd")
    denom = "uluna"
    i = 0
    while i < 10:
        # mr = ut.get_market_rate(coin, denom)
        # print(ut.convert_coin(mr))
        res = ut.swap(
            coin=coin,
            denom=denom,
        )
        time.sleep(5)
        i += 0.5
