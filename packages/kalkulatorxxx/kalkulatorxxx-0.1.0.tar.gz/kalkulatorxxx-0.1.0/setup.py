from setuptools import find_packages, setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='kalkulatorxxx',
    version='0.1.0',
    author='Jakub Cichowski',
    author_email='kubaxdd1234@wp.pl',
    packages=find_packages(),
    include_package_data=True,
    description='Simple Calculator',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown'
)
