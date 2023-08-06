from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pyStressTest',
    version='1.0',
    description='Module for resource stress testing and automatic statistics generation',
    long_description=LONG_DESCRIPTION,
    license="MIT",
    author='Chekashov Matvey/Ryize',
    author_email='chekashovmatvey@gmail.com',
    url="https://github.com/Ryize/pyStressTest",
    packages=['pyStressTest'],
    install_requires=['requests', 'matplotlib']
)
