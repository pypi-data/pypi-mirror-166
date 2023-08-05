from typing import List

from setuptools import setup, find_packages

with open("requirements.txt", "r") as requirements_file:
    requirements: List[str] = requirements_file.read().split("\n")

setup(
    name='kih_api',
    version='0.9.6',
    url='https://github.com/Kontinuum-Investment-Holdings/KIH_API',
    author='Kavindu Athaudha',
    author_email='kavindu@k-ih.co.uk',
    packages=find_packages(where="src", include=["kih_api*"]),
    package_dir={"": "src"},
    install_requires=requirements
)
