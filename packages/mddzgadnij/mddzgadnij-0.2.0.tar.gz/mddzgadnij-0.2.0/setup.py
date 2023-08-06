from setuptools import find_packages, setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='mddzgadnij',
    version='0.2.0',
    author='Dawid Mielewczyk',
    author_email='MDDawid0323@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='Tool that will try to guess your number',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown'
)
