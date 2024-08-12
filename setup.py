from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="tentorgapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=required,
    url="https://github.com/SergeyDyatlov/TentorgAPI",
    author="Sergey Dyatlov",
    author_email="",
    description="Python client library for Tentorg API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
