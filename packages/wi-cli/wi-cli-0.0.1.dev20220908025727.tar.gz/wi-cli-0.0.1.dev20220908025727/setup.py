
from setuptools import setup, find_packages
from wi.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='wi-cli',
    version=VERSION,
    description='Wi will allow storing and using a set of environment variables based on current directory',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Brent Gruber',
    author_email='me@brentgruber.net',
    url='https://github.com/BrentGruber/wi/',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'wi': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        wi = wi.main:main
    """,
)
