#!/usr/bin/env python
# Copyright (C) R O'Shaughnessy (2022)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt",'r') as f:
    lines = f.readlines()
    for indx in range(len(lines)):
        lines[indx]=lines[indx].rstrip()
REQUIREMENTS = {
  "install" : lines #["numpy>=1.14.0","scipy>=1.0.1","h5py", "corner", "numba", "scikit-learn<=0.20"]

 }

#print REQUIREMENTS
my_library_prefixes=[]
my_library_total = [("src/"+x+".py") for x in my_library_prefixes]

import glob
my_scripts = glob.glob("bin/*")


setuptools.setup(
    name="ConcordanceMMA",
    version="0.1rc1", # do not build on OSX machine, side effects
    author="Richard O'Shaughnessy",
    author_email="richard.oshaughnessy@ligo.org",
    description="Concordance pipeline for multimessenger inference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oshaughn/Concordance",
#    package_dir = {'''},
#    py_modules =set(my_library_prefixes),
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=my_scripts,
#https://docs.python.org/3/distutils/setupscript.html
# https://docs.python.org/2/distutils/setupscript.html
# Would be preferable to be *global* path, not relative to install. Depends on if doing user install or not
# This pathname puts it in the same place as the other files, in site-packages/
#   data_files=[('RIFT/likelihood',my_extra_source)],
   install_requires=REQUIREMENTS["install"]
)
