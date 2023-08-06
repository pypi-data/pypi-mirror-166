from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='mwwa',
    version='0.0.1',
    license='MIT License',
    author='Michel Rooney',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='michelrooney16@gmail.com',
    keywords='mwa',
    description=u'mwa',
    packages=['mwa'],
    install_requires=[],)