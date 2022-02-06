from src.utils import Utils
import os

if __name__ == "__main__":
    ut = Utils(chain="bombay")
    mnemonic = ut.get_mnemonic(mnemonic=os.getenv("TERRA_MNEMONIC"))
    print(mnemonic.acc_address, sep="\n")
    ut.swap(coin=ut.convert_denom(0.5), denom="uluna")
