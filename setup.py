from setuptools import setup, find_packages


def load_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="data-retrival-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=load_requirements(),
    entry_points={
        "console_scripts": [
            "dra=cli.main:main"
        ]
    },
)
