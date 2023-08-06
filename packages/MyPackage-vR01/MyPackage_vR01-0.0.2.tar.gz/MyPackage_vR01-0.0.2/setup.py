from setuptools import setup, find_packages

long_description = open("README.md", "r")

setup(
    name="MyPackage_vR01",
    description="This is my Package",
    author="Me", packages=find_packages(),
    version='0.0.2',
    long_description=long_description.read()
)

long_description.close()