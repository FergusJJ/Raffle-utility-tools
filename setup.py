from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as reqrs:
        content = reqrs.read()
        requirements = content.split('\n')
    return requirements


setup(
    name='Xntry-Scripts',
    version='0.1',
    author='Fergus Johnson',
    packages=find_packages(),
    inculde_package_data=True,
    install_requires=read_requirements(),
    entry_points='''
    [console_scripts]
    Xntry-Scripts = Xntry-Scripts.main
    '''
)