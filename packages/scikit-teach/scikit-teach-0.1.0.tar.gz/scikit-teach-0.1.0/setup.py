import pathlib
from setuptools import setup, find_packages


base_packages = ["scikit-learn>=1.0.0"]


setup(
    name="scikit-teach",
    version="0.1.0",
    author="Vincent D. Warmerdam",
    packages=find_packages(exclude=["notebooks", "docs"]),
    description="An Active Learning Approach",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://koaning.github.io/scikit-teach/",
    project_urls={
        "Documentation": "https://koaning.github.io/scikit-teach/",
        "Source Code": "https://github.com/koaning/scikit-teach/",
        "Issue Tracker": "https://github.com/koaning/scikit-teach/issues",
    },
    install_requires=base_packages,
    extras_require={"dev": []},
    license_files=("LICENSE",),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)