import setuptools
from setuptools import setup
 
setup(
    name="simple-discord-bot",
    version="1.0",
    author="Joseph Farah",
    author_email="jrfarah1999@gmail.com",
    description="Simple discord bot for the book How to Learn Python--the Wrong Way",
    long_description="Simple discord bot for the book How to Learn Python--the Wrong Way",
    long_description_content_type="text/markdown",
    url="https://github.com/jrfarah/Simple_Discord",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
    ],
    install_requires=[
        'discord.py',
    ],
)