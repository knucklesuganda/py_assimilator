from setuptools import setup, find_packages

setup(
    name='py_assimilator',
    version='0.1.0',
    author='Andrey Ivanov',
    author_email='python.on.papyrus@gmail.com',
    url='https://pypi.python.org/pypi/py_assimilator/',
    license='LICENSE.md',
    packages=find_packages(),
    description='The best python patterns for your projects',
    long_description=open('README.md').read(),
    extras_require={
        'database': ['SQLAlchemy'],
        'kafka': ['kafka-python'],
        'full': ['SQLAlchemy', 'kafka-python'],
    },
)
