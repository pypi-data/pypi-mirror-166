from setuptools import setup,find_packages

my_file = open("README.md",'r')
setup(name="myPackage-646", description="This is my package",long_description=my_file.read(), author="Me", packages=find_packages(), version='0.0.2')
my_file.close()


