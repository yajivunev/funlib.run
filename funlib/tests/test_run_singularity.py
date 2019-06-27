import unittest
import os
from funlib.run import run_singularity
from subprocess import check_call, call


class TestRunSingularity(unittest.TestCase):
    def setUp(self):
        self.singularity_image = "singularity/funlib.run_test.img"
        self.working_dir = "."
        self.mount_dirs = []
        
    def test_singularity(self):
        command = 'python3.6 ./funlib/tests/am_i_in_a_container.py'
        run_singularity(command,
                        self.singularity_image,
                        self.working_dir,
                        self.mount_dirs,
                        execute=True)

if __name__ == "__main__":
    unittest.main()
