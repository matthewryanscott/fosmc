import sys, os

from setuptools import setup, find_packages
if sys.platform == 'win32':
    #noinspection PyPackageRequirements
    import py2exe
else:
    # Not building executables on other platforms.
    py2exe = None

version = '0.417.3.14.159'


setup_kwargs = dict(
    name='fosmc',
    version=version,
    description="FosMc",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'jinja2 >= 2.6',
        'pyyaml >= 3.10',
        'slugify >= 0.0.1',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    fosmc-build = fosmc.build:main
    fosmc-lint = fosmc.lint:main
    """,
)


if py2exe:
    setup_kwargs.update(
        console=[
            'fosmc/build.py',
            'fosmc/lint.py',
        ],
    )


setup(**setup_kwargs)
