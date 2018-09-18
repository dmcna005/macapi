from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='macapi',
      scripts=['bin/alerts'],
      version='1.0.1',
      description='A python restful api access for MongoDB Atlas Cloud',
      url='https://bitbucket.org/dmcna005/macapi',
      author='Dwayne McNab',
      author_email='dmcnab@ftdi.com',
      license='GENU',
      packages=['macapi'],
      install_requires=['requests'],
      zip_safe=False)
