#!/usr/bin/env python
from setuptools import setup, find_packages


def install_requires_deps():
    with open("requirements.txt", 'r', encoding='utf-16-le') as c:
        deps = c.read()[1:].splitlines()
    return deps


setup(
    name='fat-wheel',
    version='1.0.5.beta',
    description="generate fat wheel similar to fat jar in java",
    long_description=open(r'doc/README.rst').read(),
    author='Abhinav Jain',
    author_email='ajchirawa@gmail.com',
    install_requires=install_requires_deps(),
    readme=r"doc\Readme.rst",
    license='MIT',
    # package_data={
    #     "fat_wheel": ["template/*.py", "template/*.txt"]
    # },
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "fatwheel = fat_wheel.fat:main"
        ]
    }
)
