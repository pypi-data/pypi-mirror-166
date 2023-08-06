import setuptools
from distutils.dir_util import copy_tree
from pathlib import Path
PACKAGE_NAME='strymread_lite'
import shutil, os
shutil.copy('README.md', PACKAGE_NAME + '/README.md')

def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description

v = Path(PACKAGE_NAME + "/version").open(encoding = "utf-8").read().splitlines()

setuptools.setup(
    name=PACKAGE_NAME,
    version=v[0].strip(),
    author="Alex Richardson",
    author_email="william.a.richardson@vanderbilt.edu",
    description="A real time CAN data logging tool that is a stripped down version from strym.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jmscslgroup/strymread_lite",
    packages=setuptools.find_packages(),
    install_requires=[
        l.strip() for l in Path("requirements.txt").open(encoding = "utf-8").read().splitlines()
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: AsyncIO",
        "Topic :: Communications",
        "License :: OSI Approved :: MIT License",
        ],
    keywords='candata, can, autonomous vehicle, ACC, adaptive cruise control, USB, Panda, Traffic, Transportation',
    include_package_data=True,
    package_data={'strymread_lite': ['README.md', 'dbc/*.*','version']},
    zip_safe=False
        )

os.remove(PACKAGE_NAME + '/README.md')
