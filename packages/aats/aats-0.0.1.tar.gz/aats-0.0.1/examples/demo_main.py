##############################################
#               Demo strategy                #
##############################################
import time
from aats.trade_engine import TradeEngine
from simple_maker_strategy import SimpleMakerStrategy
from simple_taker_strategy import SimpleTakerStrategy



sym_cid_map = {
    1001: "BTCUSDT.BINANCE",
    1002: "ETHUSDT.BINANCE",
    1003: "DOGEUSDT.BINANCE"
    }

# init trade engine
trade_engine = TradeEngine(sym_cid_map)

# setup public config
trade_engine.set_md_connection(ip='239.0.0.4', port=4141, use_multicast=False)  # default setting
trade_engine.add_md_symbol(symbol='BTCUSDT', exchange='BINANCE', level_num=5)
# trade_engine.add_md_symbol(symbol='DOGEUSDT', exchange='BINANCE')

# setup private config
trade_engine.set_ts_connection(ip='localhost', port=6000, use_multicast=False)  # default setting
trade_engine.config_exchange(exchange='BINANCE', trade_type='sandbox')
trade_engine.set_apikey(exchange="BINANCE", 
                        key="02SvhZEYG1p92JWdekP75XQKayqfLxmjHWNEfWU1KrCPjJ5xrLcOU1YHZ5SUBVFA", 
                        secret="iKnZvDKMGQuEINhjDX8gbIVJDLl48fV6GFLL5gcFT8Sfj9yxGrnP7uFm7AAVWeFP", 
                        password="",
                        subaccount="")
trade_engine.set_fee('BINANCE', 0.0003, 0)
trade_engine.add_trade_symbol(symbol='BTCUSDT', exchange='BINANCE', level_num=5)

# setup your strategy
# my_strategy = SimpleMakerStrategy()
my_strategy = SimpleTakerStrategy(msecs=10000)
trade_engine.add_strategy(my_strategy)

# start run
try:
    trade_engine.run()
except KeyboardInterrupt as err:
    # trade_engine.stop()
    print("close strategy and close open orders")
    # trade_engine.manager.stop()
    my_strategy.close()
    time.sleep(1)
    print("trade closed")    