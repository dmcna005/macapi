#!bin/python

"""Setup tool for macapi."""

from setuptools import setup

# import versions.py for versions display
with open('macapi/version.py') as f:
    exec(f.read())

# import readme.rst long_description file content to be displayed
with open('macapi/README.rst') as f:
    long_description = f.read()

packages = ['macapi',
            'macapi.alerts',
            'macapi.ip_whitelist'
            ]

setup(name='macapi',
      entry_points={
          'console_scripts': [
              'alerts=macapi.alerts.alerts:main'
          ]
      },
      #scripts=['bin/alerts'],
      version=__version__,
      long_description=long_description,
      url='https://bitbucket.org/dmcna005/macapi',
      author='Dwayne McNab',
      author_email='dwayneexec@gmail.com',
      description=("scripts written to interact with mongodb cloud api"),
      license='Apache 2.0',
      classifiers=[
        'Development Status :: 1 - Development',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Developers'
      ],
      packages=packages,
      install_requires=['requests'],
      zip_safe=False)
