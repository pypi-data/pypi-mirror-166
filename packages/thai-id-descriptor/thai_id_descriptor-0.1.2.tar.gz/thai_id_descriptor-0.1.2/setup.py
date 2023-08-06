import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Read long description from the readme.md file
with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="thai_id_descriptor",
    version="0.1.002",
    description="A helper package to describe about the province or area using Thai nationality ID card",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Nopporn Phantawee",
    author_email="n.phantawee@gmail.com",
    url="https://github.com/noppGithub/thai_id_descriptor",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        "black>=22.0.0",
    ],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    python_requires=">=3.6, <4",
)
