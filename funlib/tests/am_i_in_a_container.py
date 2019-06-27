import os

assert(os.environ["AM_I_IN_A_CONTAINER"]=="yes")
assert(os.environ["NV_GPU"]==str(os.environ.get("CUDA_VISIBLE_DECIVES")))
