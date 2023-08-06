from re import search
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('starksign/__init__.py') as f:
    version = search(r'version = \"(.*)\"', f.read()).group(1)

setup(
    name="starksign",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    description="SDK to facilitate Python integrations with Stark Sign",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/starksign/sdk-python",
    author="Stark Sign",
    author_email="developers@starkinfra.com",
    keywords=["stark sign", "starksign", "sdk", "stark"],
    version=version,
    install_requires=[
        "starkcore>=0.0.8",
    ],
)
