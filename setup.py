from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="tentorgapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
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
