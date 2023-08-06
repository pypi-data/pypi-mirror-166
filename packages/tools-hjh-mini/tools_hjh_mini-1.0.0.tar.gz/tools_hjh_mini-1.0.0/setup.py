from setuptools import setup

setup (
    name='tools_hjh_mini',
    version='1.0.0',
    author='HuaJunhao',
    author_email='huajunhao6@yeah.net',
    install_requires=[
          'dbutils'
        , 'pymysql'
        , 'cx_Oracle'
        , 'paramiko'
        , 'zipfile36'
        , 'crypto'
        , 'requests'
    ],
    packages=['tools_hjh_mini']
)
