"""The setup files is an essential part of the package and distributing the python projects. It is used 
by setuptools to define the configuration of your project, metadata, and dependencies. 
"""

from setuptools import setup, find_packages
from typing import List

## get the requirements from the requirements.txt file and return it as a list of strings 
def get_requirements() -> List[str]: 
    '''This function reads the requirements.txt 
    file and returns the list of requirements .'''
    ## read the requirements.txt file
    requirement_lst:List[str]=[]
    try:
        with open ('requirements.txt','r') as file:
            ## read the lines of the file
            lines= file.readlines()

            ## remove the empty lines, -e. and spaces
            requirement=[line.strip() for line in lines if line.strip() !='' and  line.strip()!='-e.']
            requirement_lst.append(requirement)
    except FileExistsError:
        print('Requirements.txt File does not exist')
    return requirement_lst

## test the function to get the requirements
print(get_requirements())


## setup the metadata of the project and the packages

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Saroj",
    author_email="me.sarojrai@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()  # Corrected the argument name
)

