from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mappyfile',
      version='0.1',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Build Tools'
      ],
      url='http://github.com/geographika/mappyfile',
      author='Seth Girvin',
      author_email='sethg@geographika.co.uk',
      license='MIT',
      packages=['mappyfile'],
      zip_safe=False)