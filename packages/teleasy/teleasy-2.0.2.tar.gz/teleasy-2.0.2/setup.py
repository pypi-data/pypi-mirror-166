from setuptools import setup, find_packages

import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
    name='teleasy',
    version='2.0.2',
    description="Creating Telegram Bots Made Simple",
    include_package_data = True,
    license='MIT',
    author="Noel Friedrich",
    author_email='noel.friedrich@outlook.de',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/noel-friedrich/teleasy',
    keywords=["telegram-bot", "bot", "telegram"],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
)