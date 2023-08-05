"""Some global corelink variables."""

DEBUG = False
valid_proto = ["ws", "tcp", "udp"]

def log(obj):
    """Logger for debug information."""
    if DEBUG:
        print("log: ", obj)

user = None
password = None
host = None
port = None
protocol = "ws"
token = None
connection = None
user_ip = None
controlID = 0
request_queue = {}
streams = {}  # # holds sender dicts with info and connection object
receiver = {}  # holds receiver dicts with info and connection object
loop = None
receiver_task = None
is_open = True
shut_down = False

async def default_cb(data, *args, key='data'):
    print("Callback not set for", key)
    if key == 'data':
        print("message:\n", data)

user_cb = default_cb
server_callbacks = {"update": default_cb, "subscriber": default_cb, "stale": default_cb, "dropped": default_cb}

