import re
from setuptools import setup
from io import open

(__version__,) = re.findall(
    '__version__ = "(.*)"', open("mappyfile/__init__.py").read()
)


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="mappyfile",
    version=__version__,
    description="A pure Python MapFile parser for working with MapServer",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Build Tools",
    ],
    package_data={"": ["*.lark"], "mappyfile": ["py.typed", "schemas/*.json"]},
    url="http://github.com/geographika/mappyfile",
    author="Seth Girvin",
    author_email="sethg@geographika.co.uk",
    license="MIT",
    packages=["mappyfile"],
    install_requires=[
        "lark>=1.1.5",
        "jsonschema>=4.18.0",
        "jsonref==1.1.0",
        "click",
    ],
    extras_require={
        "lark_cython": [
            "lark_cython>=0.0.14",
        ],
    },
    zip_safe=False,
    entry_points={
        "console_scripts": ["mappyfile=mappyfile.cli:main"],
    },
)
