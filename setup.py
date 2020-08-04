from setuptools import setup

from aiohttp_apispec_plugin.version import version

with open("README.md") as f:
    long_description = f.read()

setup(
    name="aiohttp_apispec_plugin",
    version=version,
    url="https://github.com/ckkz-it/aiohttp-apispec-plugin",
    license="MIT",
    author="Andrey Laguta",
    author_email="cirkus.kz@gmail.com",
    py_modules=["aiohttp_apispec_plugin"],
    description="APISpec plugin for aiohttp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="aiohttp apispec aiohttp_apispec_plugin",
    packages=["aiohttp_apispec_plugin"],
    python_requires=">=3.6",
    install_requires=[
        "aiohttp",
        "apispec",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Documentation",
        "License :: OSI Approved :: MIT License",
    ],
)
