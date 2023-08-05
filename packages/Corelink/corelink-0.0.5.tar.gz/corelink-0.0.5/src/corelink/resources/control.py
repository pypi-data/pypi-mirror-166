"""
Control requests that can be made from the server.
"""

from . import variables
from .reqs import retrieve, request_func


async def auth() -> int:
    """Authenticates user with values in the object
    :return: token
    """
    request = {
        "function": "auth",
        "username": variables.user,
        "password": variables.password
    }
    response = retrieve(await request_func(request), ret=True)

    variables.token = response['token']
    variables.user_ip = response['IP']

async def list_functions() -> list:
    """return: List of functions available to the user
    """
    request = {
        "function": "listFunctions",
        "token": variables.token
    }
    return retrieve(await request_func(request), "functionList")

async def list_server_functions() -> list:
    request = {
        "function": "listServerFunctions",
        "token": variables.token
    }
    return retrieve(await request_func(request), "functionList")

async def describe_function(func: str) -> dict:
    request = {"function": "describeFunction",
                "functionName": func,
                "token": variables.token}
    return retrieve(await request_func(request), "description")

async def describe_server_function() -> dict:
    request = {
        "function": "listServerFunctions",
        "token": variables.token
    }
    return retrieve(await request_func(request), "description")

async def list_workspaces() -> list:
    request = {
        "function": "listWorkspaces",
        "token": variables.token
    }
    return retrieve(await request_func(request), "workspaceList")

async def add_workspace(space: str):
    """Adds a workspace.
    :param space: Space to add
    :return: Workspace
    """
    request = {
        "function": "addWorkspace",
        "workspace": space,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def set_default_workspace(space):
    """Sets default workspace.
    :param space: space to set
    :return: Workspace
    """
    request = {
        "function": "setDefaultWorkspace",
        "workspace": space,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def get_default_workspace() -> str:
    """return: Default workspace
    """
    request = {
        "function": "getDefaultWorkspace",
        "token": variables.token
    }
    return retrieve(await request_func(request), "workspace")

async def remove_workspace(space: str):
    request = {
        "function": "rmWorkspace",
        "workspace": space,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def add_user(new_username, new_password, admin_bool, first_name,
                    last_name, email):
    request = {
        "function": "addUser",
        "username": new_username,
        "password": new_password,
        "admin": admin_bool,
        "first": first_name,
        "last": last_name,
        "email": email,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def change_password(new_password):
    request = {
        "function": "password",
        "password": new_password,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def remove_user(rm_username):
    request = {
        "function": "rmUser",
        "password": rm_username,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def list_users():
    request = {
        "function": "listUsers",
        "token": variables.token
    }
    return retrieve(await request_func(request), "userList")

async def add_group(group):
    request = {
        "function": "addGroup",
        "group": group,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def add_user_group(group, user):
    request = {
        "function": "addUserGroup",
        "group": group,
        "user": user,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def remove_user_group(group, user):
    request = {
        "function": "rmUserGroup",
        "group": group,
        "user": user,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def change_owner(group, user):
    request = {
        "function": "changeOwner",
        "group": group,
        "user": user,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def remove_group(group, user):
    request = {
        "function": "rmGroup",
        "group": group,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def list_groups(group, user):
    request = {
        "function": "listGroups",
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def list_streams(workspaces="", types=""):
    request = {
        "function": "listStreams",
        "workspaces": workspaces,
        "types": types,
        "token": variables.token
    }
    return retrieve(await request_func(request), "senderList")

async def stream_info(stream_id):
    request = {
        "function": "streamInfo",
        "streamID": stream_id,
        "token": variables.token
    }
    return retrieve(await request_func(request), "info")

async def subscribe_to_stream(receiver_id, stream_id):
    if not receiver_id in variables.receiver:
        raise Exception("Receiver not yet created.")
    request = {
        "function": "subscribe",
        "receiverID": receiver_id,
        "streamID": stream_id,
        "token": variables.token
    }
    return retrieve(await request_func(request), "streamList")

async def unsubscribe_from_stream(stream_id):
    if not stream_id in variables.receiver:
        raise Exception("Receiver not yet created.")
    request = {
        "function": "unsubscribe",
        "receiverID": variables.receiver['streamID'],
        "streamID": stream_id,
        "token": variables.token
    }
    return retrieve(await request_func(request), "streamList")

async def set_config(config, context, app, username, value):
    request = {
        "function": "setConfig",
        "config": config,
        "context": context,
        "app": app,
        "user": username,
        "value": value,
        "token": variables.token
    }
    return retrieve(await request_func(request))

async def disconnect_streams(workspaces=None, types=None, stream_ids=None):
    """Disconnects streams of given workspaces and types, or by streamIDs
    Note: if streamIDs are passed, then other params will be ignored
    return: list of disconnected streams
    """
    if not (workspaces or types or stream_ids):
        raise ValueError
    request = {
        "function": "disconnect",
        "token": variables.token
    }
    if workspaces:
        request["workspaces"] = workspaces
    if types:
        request["types"] = types
    if stream_ids:
        request["streamIDs"] = stream_ids
    return retrieve(await request_func(request), "streamList")  

# async def expire():
#     """Expires session and invalidates user token"""
#     request = {
#         "function": "expire",
#         "token": token
#     }
#     return retrieve(await request_func(request))
# Sarthak said this doesn't yet work

