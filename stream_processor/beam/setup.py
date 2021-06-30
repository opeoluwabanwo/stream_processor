"""Setup for dataflow package."""

from setuptools import find_packages, setup

REQUIRED_PACKAGES = ["Faker==8.8.2", "jsonschema==3.2.0"]

setup(
    name="stream_processor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
)
