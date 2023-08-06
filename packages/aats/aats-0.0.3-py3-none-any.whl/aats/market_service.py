import socket
import json
from enum import Enum 
from struct import pack, unpack

class NetWorkType(Enum):
    PTOP = 1
    BROADCAST = 2
    MULTICAST = 3

class MarketService(object):
    def __init__(self, sym_cid_map):
        self.sym_cid_map = sym_cid_map
        self.cid_sym_map = {v: k for k, v in self.sym_cid_map.items()}
        # self.host = socket.gethostname()
        self.ip_port = None
        self.send_to_ip = None
        self.send_to_port = None
        self.symbols = []
        self.exchanges = set()
        return

    def set_control_server(self, ip, port):
        self.control_ip = ip
        self.control_port = port

    def set_network_cfg(self, ip, port, send_type, netcard_name = ''):
        self.send_to_ip = ip
        self.send_to_port = port
        self.send_type = send_type
        self.netcard_name = netcard_name

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
                    "network": {"send_type": self.send_type.value , "network_card_name": self.netcard_name, "local_port": self.control_port, "send_to_ip": self.send_to_ip, "send_to_port": self.send_to_port}, 
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
        

