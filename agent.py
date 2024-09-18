import socket
import struct
from model import init_model
import logging
import select

class Byterator():
    def __init__(self, bytes: bytes) -> None:
        self.bytes = bytes
        self.idx = 0
        self.len = len(self.bytes)
        
    def next_float(self) -> float:
        if self.idx > self.len:
            raise IndexError("Out of Bounds")
        next = bytes(self.bytes[self.idx:self.idx+4])
        self.idx += 4
        return struct.unpack('f', next)[0]
    def next_floats(self, num) -> list[float]:
        ls = []
        for _ in range(num):
            ls.append(self.next_float())
        return ls
    def next_int32(self) -> int:
        if self.idx + 4 > self.len:
            raise IndexError("Out of Bounds")
        next = bytes(self.bytes[self.idx:self.idx+4])
        self.idx += 4
        return int.from_bytes(next)
    def next_byte(self):
        if self.idx > self.len:
            raise IndexError("Out of Bounds")
        i = self.bytes[self.idx]
        self.idx += 1
        return i

class AgentInfo():
    def __init__(self, bytes = Byterator) -> None:
        self.observations = bytes.next_byte()
        self.actions = bytes.next_byte()
class AgentPacket():
    def __init__(self, packet: Byterator, vector_size: int) -> None:
        self.last_reward = packet.next_float()
        self.input_vector = packet.next_floats(vector_size)

class Agent():
    def __init__(self, host: str = '127.0.0.1', port: int = 65432) -> None:
        self.observations = None
        self.actions = None
        self.addr = (host, port)
        self.client_socket = None
        self.open = False
        self.model = None
    
    def start_server(self):
        self.open = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(self.addr)
            server_socket.listen()
            logging.debug(f"Listening on {self.addr[0]}:{self.addr[1]}...")
            while self.open:
                self.client_socket, client_address = server_socket.accept()
                while True:
                    ready, _, _ = select.select([self.client_socket], [], [], 1)
                    if ready:
                        if self.observations == None:
                            info = self.info_packet()
                            if info != None:
                                self.observations = info.observations
                                self.actions = info.actions
                                self.model = init_model(self.observations, self.actions)
                        else:
                            packet = self.read_packet()
                            if packet != None:
                                #output = self.model(packet.input_vector)
                                print(packet.last_reward)
                    else:
                        pass
                    
    def read_packet(self) -> AgentPacket | None:
        if self.client_socket != None:
            packet_size = 4 + self.observations * 4
            data = self.client_socket.recv(packet_size)
            if not data or len(data) != packet_size:
                return
            data = Byterator(data)
            return AgentPacket(data, self.observations)
        else:
            print("No active clients")
            return
    def info_packet(self) -> AgentInfo | None:
        if self.client_socket != None:
            data = self.client_socket.recv(2)
            if not data or len(data) != 2:
                return
            data = Byterator(data)
            return AgentInfo(data)
        else:
            print("No active clients")
            return    
    def close_server(self):
        self.model.save()
        self.socket = None
        self.open = False
        
if __name__ == '__main__':
    a = Agent()
    a.start_server()