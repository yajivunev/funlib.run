from setuptools import setup

setup(
        name='funlib.run',
        version='0.1',
        description='Python wrapper for bsub',
        url='https://github.com/yajivunev/funlib.run',
        author='Nils Eckstein',
        author_email='ecksteinn@janelia.hhmi.org',
        license='MIT',
        packages=[
            'funlib.run'
        ],
        install_requires=[
            'configargparse'
        ]
)
