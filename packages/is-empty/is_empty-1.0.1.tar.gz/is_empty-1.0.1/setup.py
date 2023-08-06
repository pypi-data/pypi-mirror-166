from setuptools import setup, find_packages
import os

current_path = os.path.abspath(os.path.dirname(__file__))

def read_file(*parts):
    with open(os.path.join(current_path, *parts), encoding='utf-8') as reader:
        return reader.read()

VERSION = '1.0.1'
DESCRIPTION = 'Python package to check whether a variable is empty or not.'

# Setting up
setup(
    name="is_empty",
    version=VERSION,
    url="https://github.com/wskoly/is_empty/",
    license="MIT",
    author="Wahid Sadique Koly",
    author_email="wskoly.bp@gmail.com",
    description=DESCRIPTION,
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'variable', 'is empty', 'empty', 'length'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)