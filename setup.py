from distutils.core import setup

setup(
    name='f5abtesting',
    version='0.1.0',
    packages=['f5abtesting'],
    package_data={'f5abtesting': ['*.conf']},
    url='https://github.com/xp2014/f5abtesting',
    license='Apache License, Version 2.0',
    author='Ping Xiong',
    author_email='p.xiong@f5.com',
    description='A python package for region based abtesting'
)
