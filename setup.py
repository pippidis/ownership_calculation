from setuptools import setup, find_packages

setup(
    name="CompanyOwnership",  
    version="0.9.0",
    author="Johannes P. Lorentzen",
    author_email="pippidis@gmail.com",
    description='This is a library designed to model the dynamic changes in the distribution of company shares over time.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/pippidis/ownership_calculation",  
    packages=find_packages(exclude=['tests']), 
    install_requires=[
        "pandas",
    ],
)