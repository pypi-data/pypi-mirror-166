from __future__ import annotations

import setuptools


def read_readme() -> str:
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="deltadash",
    version="0.1.0",
    description="A simple parser library for the game DeltaDash.",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.6",
    url="https://github.com/RealistikDash/deltadash.py",
    project_urls={
        "GitHub: repo": "https://github.com/RealistikDash/deltadash.py",
        "GitHub: issues": "https://github.com/RealistikDash/deltadash.py/issues",
    },
    long_description_content_type="text/markdown",
    long_description=read_readme(),
    packages=setuptools.find_packages(),
)
