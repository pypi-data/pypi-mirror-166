"""Some more backend processing functions."""

from socket import SOCK_DGRAM, socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import ssl
import asyncio
import websockets
import json
from .Proto import Proto
from .reqs import receiver_callback
from . import variables

async def ws_control_receiver(stream):
    variables.log("[WS] control receiver channel open.")
    async for message in stream:
        asyncio.create_task(response(message))

async def ws_receiver(stream):
    variables.log('[WS] Receiver connected.')
    async for message in stream['connection']:
        asyncio.create_task(receiver_callback(message))

async def response(response) -> dict:
    """Processes server response and relays server control functions away"""
    variables.log("response received")
    response = json.loads(response)
    if 'function' in response:
        await variables.server_callbacks[response['function']](response, key=response['function'])
    elif 'ID' in response:
        variables.request_queue[response['ID']] = response
        del response['ID']

async def connect_sender(streamID):
    """Connects sender in order to send data"""
    stream = variables.streams[streamID] # for convenience
    if stream['protocol'] == 'tcp':
        stream['connection'] = socket(AF_INET, SOCK_STREAM)
        stream['connection'].connect((variables.host, int(stream['port'])))
    elif stream['protocol'] == 'udp':
        stream['connection'] = socket(AF_INET, SOCK_DGRAM)
        stream['connection'].connect((variables.host, int(stream['port'])))
    elif stream['protocol'] == 'ws':
        stream['connection'] = await websockets.connect(f"wss://{variables.host}:{stream['port']}",
                                                        ssl=ssl.SSLContext(ssl.PROTOCOL_TLS))
        variables.log('connected WS sender.')

async def connect_receiver(streamID):
    """Connects receiver in order to send data."""
    receiver = variables.receiver[streamID]  # for convenience
    variables.log(receiver)

    header = [0, 0, 0, 0, 0, 0, 0, 0]
    header = bytearray(header)
    head = memoryview(header)
    head[4:6] = int.to_bytes(int(streamID), 2, 'little')
    header = bytes(header)
    variables.log(header)

    if receiver['proto'] == 'tcp':
        receiver['connection'] = await variables.loop.create_connection(lambda: Proto(header, 'tcp', int(receiver['port'])), 
                                                                    variables.host, int(receiver['port']))
    elif receiver['proto'] == 'udp':
        receiver['connection'] = await variables.loop.create_datagram_endpoint(lambda: Proto(header, 'udp', int(receiver['port'])),
                                                                        remote_addr=(variables.host, int(receiver['port'])))
    elif receiver['proto'] == 'ws':
        receiver['connection'] = await websockets.connect(f"wss://{variables.host}:{receiver['port']}", 
                                    ssl=ssl.SSLContext(ssl.PROTOCOL_TLS))
        await receiver['connection'].send(header)
        variables.receiver_task = asyncio.create_task(ws_receiver(receiver))

async def maintain():
    while not variables.shut_down:
        await asyncio.sleep(0)