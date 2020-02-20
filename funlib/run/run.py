from funlib.run.run_singularity import run_singularity
from subprocess import check_call
import configargparse
import logging
import os
import random

logger = logging.getLogger(__name__)

p = configargparse.ArgParser(default_config_files=['~/.pysub'])

p.add('-p', required=True,
      help="The command to run" +
      " e.g. ``python train.py``.")

p.add('-c', '--num_cpus', required=False, type=int,
      help="Number of CPUs to request, default 5.",
      default=5)

p.add('-g', '--num_gpus', required=False, type=int,
      help="Number of GPUs to request, default 1.",
      default=1)

p.add('-m', '--memory', required=False, type=int,
      help="Amount of memory [MB] to request, default 25600.",
      default=25600)

p.add('-w', '--working_directory', required=False,
      help="The working directory for <command>," +
           "defaults to current directory",
      default=".")

p.add('-s', '--singularity', required=False,
      help="Optional singularity image to use to" +
           "execute <command>. The singularity" +
           "container will have some common local" +
           "directories mounted. See ``~/.deploy``.",
      default="")

p.add('-o', '--host', required=False,
      help="Ensure that the job is placed on the given host.",
      default="")

p.add('-q', '--queue', required=False,
      help="Use the given queue.",
      default="normal")

p.add('-e', '--environment', required=False,
      help="Environmental variable.",
      default="")

p.add('-b', '--batch', required=False, action='store_true',
      help="If given run command in background." +
           "This uses sbatch to submit" +
           "a task, see the status with bjobs. If not given, this call" +
           "will block and return the exit code of <command>.")

p.add('-d', '--mount_dirs', nargs='*',
      help="Directories to mount in container."
           " If multiple, separate with space",
      default=[])

p.add('-j', '--job_name', required=False,
      help="Name of job to submit",
      default="")

p.add('-a', '--array_size', required=False, type=int,
      help="Array size larger than 1 indicates an array job. Default is 1, "
           "for a normal non-array job. Use \\$LSB_JOBINDEX to reference "
           "the index, for example, to read a different config file "
           "for each job in the array",
      default=1)

p.add('-l', '--array_limit', required=False, type=int,
      help="Number of jobs in the array to run at once. Default is"
           " no limit.",
      default="")

p.add('-lg', '--log_file', required=False,
      help="Name of log file for std out.",
      default=None)

p.add('-nw', '--no_wait', action='store_false',
      help="If given, don't block after submitting array jobs. Default is"
           " to call bwait after array jobs to block until array job"
           "is done. You must check exit status of each job individually.")


def run(command,
        num_cpus=5,
        num_gpus=1,
        memory=25600,
        working_dir=".",
        singularity_image="",
        host="",
        queue="normal",
        environment_variable="",
        batch=False,
        mount_dirs=[],
        execute=False,
        expand=True,
        job_name="",
        array_size=1,
        array_limit=None,
        log_file=None,
        no_wait=False):

    if not singularity_image or singularity_image == "None":
        comment = ""
    else:
        container_id = random.randint(0, 32767)
        os.environ["CONTAINER_NAME"] = "{}_{}".format(os.environ.get('USER'),
                                                      container_id)
        comment = '"{}|{}"'.format(singularity_image, container_id)
        if environment_variable == "None":
            environment_variable = ""
        command = environment_variable + command
        command = run_singularity(command, singularity_image,
                                  working_dir, mount_dirs)

    if execute:
        logger.info("Scheduling job on {} CPUs, {} GPUs.".format(
                        num_cpus, num_gpus) +
                    " {} MB with container '{}' in working dir '{}'".format(
                        memory, singularity_image, working_dir))

    if log_file:
        log = "-o {}".format(log_file)
    else:
        log = "-o %J.log"

    if not batch:
        submit_cmd = 'bsub -I -R "affinity[core(1)]"'
    elif array_size > 1:
        submit_cmd = 'bsub -R "affinity[core(1)]" ' + log
        if not no_wait:
            bwait = "bwait -w 'ended({})'"
    else:
        submit_cmd = 'bsub -K -R "affinity[core(1)]" ' + log

    if num_gpus <= 0:
        use_gpus = ""
    else:
        use_gpus = '-gpu "num={}:mps=no"'.format(num_gpus)

    if not host or host == "None":
        use_host = ""
        host = ""
    else:
        use_host = "-m"

    run_command = [submit_cmd]

    if comment and not job_name:
        job_name = comment

    if array_size > 1:
        if not job_name:
            job_name = 'array_job'
        if not no_wait:
            bwait = bwait.format(job_name)
        job_name += "[1-{}]".format(array_size)
        if array_limit:
            job_name += "%{}".format(array_limit)

    if job_name:
        run_command += ['-J "{}"'.format(job_name)]
    run_command += ["-n {}".format(num_cpus)]
    run_command += [use_gpus]
    run_command += ['-R "rusage[mem={}]"'.format(memory)]
    run_command += ["-q {}".format(queue)]
    run_command += ["{} {}".format(use_host, host)]
    run_command += [command]

    if not execute:
        if not expand:
            return run_command
        else:
            return ' '.join(run_command)
    else:
        run_command = ' '.join(run_command)
        check_call(run_command,
                   shell=True)
        if bwait:
            check_call(bwait,
                       shell=True)


if __name__ == "__main__":
    options = p.parse_args()

    command = options.p
    num_cpus = options.num_cpus
    num_gpus = options.num_gpus
    memory = options.memory
    working_dir = options.working_directory
    singularity_image = options.singularity
    host = options.host
    queue = options.queue
    environment_variable = options.environment
    batch = options.batch
    mount_dirs = options.mount_dirs
    execute = True
    expand = True
    job_name = options.job_name
    array_size = options.array_size
    array_limit = options.array_limit
    no_wait = options.no_wait

    run(command,
        num_cpus,
        num_gpus,
        memory,
        working_dir,
        singularity_image,
        host,
        queue,
        environment_variable,
        batch,
        mount_dirs,
        execute,
        expand,
        job_name,
        array_size,
        array_limit,
        no_wait)
