#!/usr/bin/env python

from setuptools import setup, find_packages

# setup the project
setup(
    name="django-selenium-testcase",
    version="1.3.2",
    author="Nimbis Services, Inc.",
    author_email="info@nimbisservices.com",
    description="Selenium helper methods for Django live server testing.",
    license="BSD",
    packages=find_packages(exclude=["test_project", ]),
    install_requires=[
        'Django',
        'selenium>=4'
    ],
    zip_safe=False,
    include_package_data=True,
)
