from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="TV Shows Tracker",
    description="Tool to get informed of new releases of your favourite TV shows",
    version="1",
    long_description=readme(),
    install_requires=["requests", "pymongo", "simple-term-menu"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tv-shows-tracker=src.main:main",
        ]
    },
)
