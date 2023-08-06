import sys
sys.path.insert(0,'/home/zhangtian/dev/algo-client-api/src/')

from aats.market_service import MarketService
from aats.market_service import NetWorkType

# maintain your unique cid symbol mapping table which needs to be consistent in both market engine and trade engine
sym_cid_map = {
    1001: "BTCUSDT.BINANCE",
    1002: "ETHUSDT.BINANCE",
    1003: "DOGEUSDT.BINANCE",
    1004: "BTCUSDTSWAP.BINANCE_SWAP"
    }

# start market engine
mkt_engine = MarketService(sym_cid_map)
mkt_engine.set_control_server(ip='127.0.0.1', port=8060)  # default setting
mkt_engine.set_network_cfg(ip='127.0.0.1', port=7624, send_type=NetWorkType.PTOP, netcard_name = '')
mkt_engine.add_listen_symbol('BTCUSDT', 'BINANCE', 5)
mkt_engine.add_listen_symbol('ETHUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('DOGEUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('BTCUSDTSWAP', 'BINANCE_SWAP', 5)
mkt_engine.run()