from setuptools import setup, find_packages

my_file = open('README.md', 'r')
setup(name='MyPackage-118', description='This is my package', author='Andrei', packages=find_packages(), version='0.0.1', long_description=my_file.read())
my_file.close()