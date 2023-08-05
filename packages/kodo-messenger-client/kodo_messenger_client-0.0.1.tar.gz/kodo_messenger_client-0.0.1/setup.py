from setuptools import setup, find_packages

setup(
    name='kodo_messenger_client',
    version='0.0.1',
    description='kodo_messenger_client',
    author='Roman Kodoch',
    author_email='kodochigovra@mail.ru',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptdome', 'pycryptdomex']
)
