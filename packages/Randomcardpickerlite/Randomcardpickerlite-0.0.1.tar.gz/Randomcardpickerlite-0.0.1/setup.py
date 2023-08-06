from setuptools import find_packages, setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='Randomcardpickerlite',
    version='0.0.1',
    author='Borys Paisny',
    author_email='BorysPiasny@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='pick a random card',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown'
)
