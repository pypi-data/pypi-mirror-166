from setuptools import setup, find_packages
VERSION = '1.0.0'
DESCRIPTION = 'A Poly Bridge 2 format parser'
LONG_DESCRIPTION = '''
This is a library that allows you to easily parse Poly Bridge 2 .layout and .slot files.
'''

setup(
    name="pylybridge",
    version=VERSION,
    author="ashduino101",
    author_email="<ashduino101@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "setuptools>=42",
        "wheel",
        "pillow",
    ],
    keywords=["python", "polybridge", "api", "wrapper", "polybridge2", "polybridge2api", "game"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ]
)
