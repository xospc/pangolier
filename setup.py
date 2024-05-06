from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pangolier',
    version='0.2.3',
    packages=find_packages(include=['pangolier']),
    package_data={
        'pangolier': ['py.typed'],
    },
    python_requires='>=3.10',

    url='https://pangolier.readthedocs.io',
    description='build PromQL by Python code',
    long_description_content_type='text/markdown',
    long_description=long_description,

    project_urls={
        'Documentation': 'https://pangolier.readthedocs.io',
        'Source': 'https://github.com/lexdene/pangolier',
    },
)
