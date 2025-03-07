from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="myenergi",
    version="0.0.1",
    author="Skywatcher",
    author_email="integrations@skywatcher.uk",
    description="A small package to work with MyEnergi API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skywatcher-uk/myenergi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ]
)