from setuptools import setup, find_packages
import io
import os

VERSION = "0.1a"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="conditional-get",
    description="CLI tool for fetching data using HTTP conditional get",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(),
    install_requires=["httpx", "click"],
    extras_require={"test": ["pytest", "pytest-mock"]},
    tests_require=["conditional-get[test]"],
    entry_points="""
        [console_scripts]
        conditional-get=conditional_get.cli:cli
    """,
    url="https://github.com/simonw/conditional-get",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
