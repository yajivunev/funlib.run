import unittest
import os
from funlib.run import run
from subprocess import check_call


class TestRun(unittest.TestCase):
    def setUp(self):
        self.singularity_image = "singularity/funlib.run_test.img"
        self.working_dir = "."
        self.mount_dirs = []
        
    def test_submit(self):
        command = 'python3.6 ./funlib/tests/am_i_in_a_container.py'
        run(command,
            num_cpus=5,
            num_gpus=1,
            memory=25600,
            working_dir=self.working_dir,
            singularity_image=self.singularity_image,
            host="",
            queue="slowpoke",
            execute=True)

    def test_host(self):
        command = 'python3.6 ./funlib/tests/am_i_on_my_host.py'
        run(command,
            num_cpus=1,
            num_gpus=0,
            memory=25600,
            working_dir=self.working_dir,
            singularity_image=self.singularity_image,
            host="c04u21",
            queue="slowpoke",
            execute=True)

    def test_mount(self):
        command = 'python3.6 ./funlib/tests/am_i_mounted.py'
        run(command,
            num_cpus=1,
            num_gpus=0,
            memory=25600,
            working_dir=self.working_dir,
            singularity_image=self.singularity_image,
            host="",
            queue="slowpoke",
            mount_dirs=["/nrs", "/tmp"],
            execute=True)


if __name__ == "__main__":
    unittest.main()
