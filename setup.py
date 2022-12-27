from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pangolier',
    version='0.0.4',
    packages=find_packages(include=['pangolier']),
    python_requires='>3.10.0',

    url='https://github.com/lexdene/pangolier',
    description='prometheus query builder',
    long_description_content_type='text/markdown',
    long_description=long_description,
)
