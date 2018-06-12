from setuptools import setup

setup(
    name='address-book-api',
    version='0.1',
    description='An API for storing contacts with elasticsearch.',
    author='Alex Nordstrom',
    author_email='a.l.nordstrom@gmail.com',
    install_requires=['flask', 'elasticsearch']
)