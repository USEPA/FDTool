import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('fdtool/fdtool.py').read(),
    re.M
    ).group(1)
"""
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
"""

setup(name='fdtool',
        version= version,
        packages = ["fdtool"],
        entry_points = {
        "console_scripts": ['fdtool = fdtool.fdtool:main']
        },
        description='Identify functional dependencies, equivalences, and candidate keys in tabular data',
        #long_description = long_descr,
        url='https://github.com/USEPA/FDTool/',
        author='Matt Buranosky',
        include_package_data=True,
        package_data={'fdtool':['modules/*.py']},
        author_email='buranosky.matthew@epa.gov',
        license='CC0',
        zip_safe=False)
