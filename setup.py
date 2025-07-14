from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tree-allometry",
    version="0.1.0",
    author="Tree Allometry Project",
    author_email="example@example.com",
    description="A Python package for tree allometric calculations based on biomass modeling systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/tree-allometry",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "sphinx>=3.0",
            "black",
            "flake8",
        ],
    },
    include_package_data=True,
    package_data={
        "tree_allometry": ["data/*.csv"],
    },
)