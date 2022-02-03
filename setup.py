#!/usr/bin/env python

from setuptools import setup

setup(
    name="tap-public-holidays",
    version="1.0.0",
    description="Singer.io tap for extracting data from the publicholidays.co.nz site",
    author="Sam Woolerton",
    url="https://samwoolerton.com",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_public_holidays"],
    install_requires=[
        "singer-python==5.9.0",
        "beautifulsoup4==4.10.0",
        "requests==2.27.1",
    ],
    extras_require={
        "dev": [
            "pylint",
            "ipdb",
            "nose",
        ]
    },
    entry_points="""
          [console_scripts]
          tap-public-holidays=tap_public_holidays:main
      """,
    packages=["tap_public_holidays"],
    package_data={"tap_public_holidays": ["tap_public_holidays/schemas/*.json"]},
    include_package_data=True,
)
