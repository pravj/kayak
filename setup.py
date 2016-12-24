from setuptools import setup

setup(name='kayak',
      version='0.0.9.dev.k',
      description='A customizable Twitter client to collect tweets matching certain criteria',
      url='http://github.com/pravj/kayak',
      author='Pravendra Singh',
      author_email='hackpravj@gmail.com',
      license='GNU GENERAL PUBLIC LICENSE - version 3',
      install_requires=[
          'requests>=2.12.4',
          'wheel>=0.24.0'
      ],
      packages=['kayak.client', 'kayak.auth'])
