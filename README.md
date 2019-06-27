# funlib.run
Python wrapper for submitting jobs via bsub with the option to do so in a container environment. 

## Setup
```
make install-full
```

This creates a funlib.run config file ~/.funlib.run
that contains default parameters that
can be overwritten for each specific run:
```
num_gpus = 1
memory = 25600
working_directory = .
singularity = ""
host = ""
queue = "normal"
environment = ""
batch = False
mount_dirs = ""
```

## Usage
There are three useful ways to use funlib.run:

1. Direct usage via command line arguments (overwrites config file defaults):
```bash
python run.py -p "python train.py" -c 5 -g 1 -q normal -s path-to-singularity-image

python run_singularity.py -p "python mknet.py" -s path-to-singularity-image
```

2. Indirect call via another script:
```python
from funlib.run import run, run_singularity

run(command="python train.py",
    num_cpus=5,
    num_gpus=1,
    queue="normal",
    execute=True)

run_singularity(command="python mknet.py",
                singularity_image="path_to_image",
                execute=True)
```

3. Command creation and subsequent call:
```python
from funlib.run import run, run_singularity
from subprocess import check_call

run_command = run(command="python train.py",
                  num_cpus=5,
                  num_gpus=1,
                  queue="normal",
                  execute=False)

check_call(run_command,
           shell=True)

run_singularity_command = run_singularity(command="python mknet.py",
                                          singularity_image="path_to_image",
                                          execute=False)

check_call(run_singularity_command,
           shell=True)
```

## Usage with Daisy
When used with daisy.call do not expand the cmd to a string via setting expand=False:
```python
cmd = run(command=base_command,
          queue=queue,
          num_gpus=1,
          num_cpus=num_cpus,
          singularity_image=singularity_container,
          mount_dirs=mount_dirs,
          execute=False,
          expand=False)

daisy.call(cmd, log_out=log_out, log_err=log_err)
```
