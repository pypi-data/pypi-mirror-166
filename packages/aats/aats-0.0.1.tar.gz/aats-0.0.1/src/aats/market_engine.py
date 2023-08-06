import socket
import json
from struct import pack, unpack

class MarketEngine(object):
    def __init__(self, sym_cid_map):
        self.sym_cid_map = sym_cid_map
        self.cid_sym_map = {v: k for k, v in self.sym_cid_map.items()}
        # self.host = socket.gethostname()
        self.ip_port = None
        self.mcast_grp = None
        self.mcast_port = None
        self.symbols = []
        self.exchanges = set()
        return

    def set_control_server(self, ip, port):
        self.control_ip = ip
        self.control_port = port

    def set_network_cfg(self, ip, port, use_multicast=False):
        self.mcast_grp = ip
        self.mcast_port = port
        self.use_multicast = use_multicast

    def add_listen_symbol(self, symbol, exchange, book_level):
        cid = self.cid_sym_map[symbol+'.'+exchange]
        self.symbols.append({'cid': cid, 'port': [symbol, exchange], 'book_level': book_level})
        self.exchanges.add(exchange)

    def send_msg(self, msg, socket):
        message_len = len(msg)
        message_format = '>i' + str(message_len) + 's'
        send_message = pack(message_format, message_len,msg.encode('utf-8'))
        socket.send(send_message)

    def run(self):
        self.server_socket = socket.socket()
        self.server_socket.connect((self.control_ip, self.control_port))
        # request new instance and wait for pin and instance port
        msg = {"type": "new_market_instance", 
                "cfg": {
                    "instance": {"license_id": "TRAIL001", "license_key": "apifiny123456", "log_path": "/data/cc/trader_service", "log_level": 1, "name": "trader_service", "book_depth": 5}, 
                    "servers": {"redis_server": "127.0.0.1"}, 
                    "multibroad": {"network_card_name": "PC1", "local_port": self.control_port, "multicast_ip": self.mcast_grp, "multicast_port": self.mcast_port}, 
                    "exchanges": [{"exchange": exch} for exch in self.exchanges], 
                    "symbols": self.symbols}
                    }
        # print(msg)
        msg = json.dumps(msg)
        self.send_msg(msg, self.server_socket)
        data = self.server_socket.recv(1024)
        # print(data)
        length = unpack('i', data[:4])[0]
        resp = json.loads(data[4:length+4].decode('utf-8'))
        print(resp)
        

