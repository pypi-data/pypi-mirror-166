"""
This is the official python module for interfacing with a Corelink server.
Details regarding the Corelink project can be found at [corelink.hpc.nyu.edu](https://corelink.hpc.nyu.edu).

This package is split into two submodules:
- `corelink.corelink` contains the main client-facing Corelink functions
- `corelink.resources` contains other functions and processes in the background of corelink
- notably, `corelink.resources.control` contains all the possible Corelink control functions a user can send.

All functions in `corelink.corelink` and `corelink.resources.control` are migrated into the main `corelink` namespace.
"""
from .corelink import *
from .resources.control import *
# or:
#     from .resources import control
# for namespace separation