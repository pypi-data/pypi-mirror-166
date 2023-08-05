import asyncio
from .variables import log
from .reqs import receiver_callback

class Proto(asyncio.Protocol):
    """An asyncio Protocol class used to process incoming messages for a receiver.
    Implements TCP or UDP protocol."""
    def __init__(self, message: bytearray, type, port) -> None:
        self.header = bytes(message)
        self.type = type
        self.transport = None
        self.port = port

    def connection_made(self, transport) -> None:
        self.transport = transport
        if self.type == 'tcp':
            self.transport.write(self.header)
        else:
            print(self.port)
            self.transport.sendto(self.header)
        log(f"[{self.type}] Receiver connected. Waiting for data.")
            
    def connection_lost(self, exc):
        log('The server closed the connection')
    
    #TCP
    def data_received(self, data: bytes) -> None:
        log("[tcp] data received")
        asyncio.create_task(receiver_callback(data))

    #UDP
    def datagram_received(self, data, addr):
        log("[udp] data received")
        asyncio.create_task(receiver_callback(data))

    #UDP
    def error_received(self, exc):
        print('Error received:', exc)