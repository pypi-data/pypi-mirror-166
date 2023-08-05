from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AutoDocker",
    version="0.2.0",
    author="Abhishek Kognole",
    author_email="aakognole@gmail.com",
    description="Simple program to quickly dock ligands using Autodock Vina",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aakognole/autodocker",
    project_urls={
        "Bug Tracker": "https://github.com/aakognole/autodocker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=['rdkit-pypi'],
    python_requires=">=3.6",
    zip_safe=False
)
