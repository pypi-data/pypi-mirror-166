from setuptools import setup, find_packages # importam setarile pentru un pachet din pachetul instalat in terminal
my_file = open('README.md', 'r')

setup(name='Mypackage-665', description='This is my package', long_description=my_file.read(), author='me', packages=find_packages(), version='0.0.2')
my_file.close()