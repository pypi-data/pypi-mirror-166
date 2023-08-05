from setuptools import setup, find_packages

setup(
    name='kodo_messenger_server',
    version='0.0.4',
    description='kodo_messenger_server',
    author='Roman Kodoch',
    author_email='kodochigovra@mail.ru',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy']
)
