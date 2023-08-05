from setuptools import setup, find_packages

setup(name="py_test_client_chat_358",
      version="0.0.2",
      description="Mess Client",
      author="Ivan Ivanov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycrypto']
      )