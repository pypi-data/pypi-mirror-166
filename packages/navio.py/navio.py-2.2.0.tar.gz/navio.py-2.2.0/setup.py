from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="navio.py",
    version="2.2.0",
    description="Simple API Wrapper for the Navio API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrbean565/Navio-Integration/tree/main/navio",
    author="Bean",
    author_email="bean@truckerbean.com",
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords="api wrapper",
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        'requests'
        ],
)
