from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mappyfile',
      version='0.1.3',
      description='A pure Python MapFile parser for working with MapServer',
      long_description=readme(),
      classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Build Tools'
      ],
      package_data = {
        '': ['*.g']
      },
      url='http://github.com/geographika/mappyfile',
      author='Seth Girvin',
      author_email='sethg@geographika.co.uk',
      license='MIT',
      packages=['mappyfile'],
      install_requires=['plyplus'],
      zip_safe=False)