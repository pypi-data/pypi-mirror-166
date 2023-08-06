from aats.market_engine import MarketEngine

# maintain your unique cid symbol mapping table which needs to be consistent in both market engine and trade engine
sym_cid_map = {
    1001: "BTCUSDT.BINANCE",
    1002: "ETHUSDT.BINANCE",
    1003: "DOGEUSDT.BINANCE",
    1004: "BTCUSDTSWAP.BINANCE_SWAP"
    }

# start market engine
mkt_engine = MarketEngine(sym_cid_map)
mkt_engine.set_control_server(ip='localhost', port=6000)  # default setting
mkt_engine.set_network_cfg(ip='239.0.0.4', port=4141, use_multicast=False)
mkt_engine.add_listen_symbol('BTCUSDT', 'BINANCE', 5)
mkt_engine.add_listen_symbol('ETHUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('DOGEUSDT', 'BINANCE', 5)
# mkt_engine.add_listen_symbol('BTCUSDTSWAP', 'BINANCE_SWAP', 5)
mkt_engine.run()