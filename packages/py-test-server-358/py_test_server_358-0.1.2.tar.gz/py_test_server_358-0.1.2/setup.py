from setuptools import setup, find_packages

setup(name="py_test_server_358",
      version="0.1.2",
      description="Mess Server",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycrypto'],
      scripts=['server/server_run.py']
      )