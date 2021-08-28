import re
from setuptools import setup
from io import open

__version__, = re.findall('__version__ = "(.*)"',
                          open('mappyfile/__init__.py').read())

def readme():
    with open('README.rst', "r", encoding="utf-8") as f:
        return f.read()


setup(name='mappyfile',
      version=__version__,
      description='A pure Python MapFile parser for working with MapServer',
      long_description=readme(),
      classifiers=[
          # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Intended Audience :: Developers',
          'Topic :: Text Processing :: Linguistic',
          'Topic :: Software Development :: Build Tools'
      ],
      package_data={
          '': ['*.g'],
          'mappyfile': ['schemas/*.json']
      },
      url='http://github.com/geographika/mappyfile',
      author='Seth Girvin',
      author_email='sethg@geographika.co.uk',
      license='MIT',
      packages=['mappyfile'],
      install_requires=[
            'lark-parser>=0.11.3',
            # pyrsistent is a dependency of jsonschema but py2 is not
            # supported beyond 0.16.0
            'pyrsistent<0.17.0; python_version=="2.7"',
            'jsonschema>=2.0, <=3.2.0',
            'jsonref==0.2',
            'click; python_version>="3.0.0"',
            'click < 8.0.0; python_version=="2.7"'
      ],
      zip_safe=False,
      entry_points = {
        'console_scripts': ['mappyfile=mappyfile.cli:main'],
    }
)
