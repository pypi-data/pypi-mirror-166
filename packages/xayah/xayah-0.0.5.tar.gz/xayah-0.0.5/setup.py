from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xayah',
    url='https://github.com/ualisars/xayah',
    version='0.0.5',
    description='A lightweight testing tool with test report functionality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(
        where='src',
        include=['xayah*']
    ),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pydantic == 1.7.3'
    ]
)
