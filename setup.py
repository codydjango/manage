from setuptools import setup, find_packages

with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setup(
    name='em',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'em=em.mng:main',
        ],
    },
)