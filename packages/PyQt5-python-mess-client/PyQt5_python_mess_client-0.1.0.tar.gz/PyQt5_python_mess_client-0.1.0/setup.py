from setuptools import setup, find_packages

setup(name="PyQt5_python_mess_client",
      version="0.1.0",
      description="messaging messenger",
      author="Alex Devalt",
      author_email="alla.mihelson@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
