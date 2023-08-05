"""Data retireval functions."""

from . import variables
import json
import asyncio

async def request_func(command: dict) -> dict:
    """Sends control function to server
    :param command: request to be send
    """
    variables.log("requesting: "+ str(command))
    command['ID'] = variables.controlID
    variables.request_queue[variables.controlID] = False
    variables.controlID += 1
    await variables.connection.send(json.dumps(command))
    while not variables.request_queue[command['ID']]:
        await asyncio.sleep(.05)
    ret = variables.request_queue[command['ID']]
    del variables.request_queue[command['ID']]
    return ret

def retrieve(response, key=None, ret=False):
    variables.log("retrieving data")
    if response["statusCode"] == 0:
        if ret:
            return response
        elif key is None:
            return 0
        else:
            try:
                return response[key]
            except KeyError:
                raise KeyError("Data retrieval failed.")
    raise Exception("request returned with status code " + str(response['statusCode']) + ":\n" + response['message'])

async def receiver_callback(message: bytes):
    variables.log('in receiver_callback()')
    head_size = int.from_bytes(message[:2], 'little')
    if head_size:
        header = json.loads(message[8:head_size+8])
    else:
        header = {}
    streamID = int.from_bytes(message[4:6], 'little')
    message = message[8+head_size:]
    await variables.user_cb(message, streamID, header)

    