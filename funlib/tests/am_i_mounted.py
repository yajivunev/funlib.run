import os

assert(os.environ["AM_I_IN_A_CONTAINER"]=="yes")
assert(os.path.exists("/tmp"))
assert(os.path.exists("/nrs"))
