from setuptools import setup, find_packages

setup(
    name='py_assimilator',
    version='0.3.1',
    author='Andrey Ivanov',
    author_email='python.on.papyrus@gmail.com',
    url='https://pypi.python.org/pypi/py_assimilator/',
    project_urls={
        'Documentation': 'https://knucklesuganda.github.io/py_assimilator/',
        'Github': 'https://github.com/knucklesuganda/py_assimilator',
        'Youtube RU': 'https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw',
        'Youtube ENG': 'https://www.youtube.com/channel/UCeC9LNDwRP9OfjyOFHaSikA',
    },
    license='LICENSE.md',
    packages=find_packages(),
    description='The best python patterns for your projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    requires=['pydantic>=1.10.2'],
    extras_require={
        'database': ['SQLAlchemy>=1.4.44'],
        'kafka': ['kafka-python>=2.0.2'],
        'redis': ['redis>=4.4.0'],
        'mongo': ['pymongo>=4.3.3'],    # TODO: fix optional
    },
)
