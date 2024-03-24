from setuptools import setup, find_packages

setup(
    name='relevant-search-results',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        "urltotext==0.3.0",
        "llama-index==0.10.20",
        "googlesearch-python==1.2.3",
    ],
    # Additional metadata about your package.
    author='Chinmay Shrivastava',
    author_email='cshrivastava99@gmail.com',
    description='#',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)