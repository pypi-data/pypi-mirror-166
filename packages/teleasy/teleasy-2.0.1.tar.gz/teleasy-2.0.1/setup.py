from setuptools import setup, find_packages

setup(
    name='teleasy',
    version='2.0.1',
    description="Creating Telegram Bots Made Simple",
    include_package_data = True,
    license='MIT',
    author="Noel Friedrich",
    author_email='noel.friedrich@outlook.de',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/noel-friedrich/teleasy',
    keywords='telegram bot telegram-bot',
    install_requires=[],
)